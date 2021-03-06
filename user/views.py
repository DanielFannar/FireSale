import datetime

from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

from user.forms.message_form import MessageCreateForm
from user.forms.profile_form import ProfileCreateForm, ProfileUpdateForm
from user.forms.rating_form import RatingCreateForm
from user.models import UserProfile, Rating, Message, Notification, UserSettings
from user import helper_functions


def register(request):
    """This view lets a user register a new account."""
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileCreateForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            settings = UserSettings(email_notification=True)
            user.email = request.POST['email']
            user.save()
            settings.save()
            profile.user = user
            profile.settings = settings
            profile.save()
            messages.success(request, 'Successfully registered! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Error in registration.')
            return redirect('register')
    else:
        return render(request, 'user/register.html', {
            'user_form': UserCreationForm(),
            'profile_form': ProfileCreateForm()
        })

@login_required
def get_profile(request, user_id=None):
    """This view lets a user see detailed information about a user."""
    current_user = request.user
    if user_id is None:
        user_id = request.user.id
    user = get_object_or_404(User, pk=user_id)
    if current_user == user:
        displayed_name = 'Your'
    else:
        displayed_name = str(user)+"'s"
    return render(request, 'user/profile.html', {
        'current_user': current_user,
        'user': user,
        'user_profile': get_object_or_404(UserProfile.objects.select_related(), user_id=user_id),
        'displayed_name': displayed_name
    })

@login_required
def edit_profile(request):
    """This view lets a user edit their profile information."""
    user = get_object_or_404(User, pk=request.user.id)
    user_profile = get_object_or_404(UserProfile.objects.select_related(), user_id=user.id)
    if request.method == 'POST':
        form = ProfileUpdateForm(data=request.POST,
                                 instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            settings = profile.settings
            if 'email_notifications' in request.POST:
                settings.email_notification = True
            else:
                settings.email_notification = False
            profile.save()
            settings.save()
            messages.success(request, 'Profile edited!')
            return redirect('my-profile')
        else:
            messages.error(request, 'Profile could not be edited')
            return redirect('my-profile')
    else:
        form = ProfileUpdateForm(instance=user_profile,
                                 initial={'email': user.email, 'settings': user_profile.settings.email_notification})
        return render(request, 'user/edit_profile.html', {
            'form': form
        })

@login_required
def get_user_ratings(request, user_id):
    """This view lets a user see all ratings for a particular user."""
    user = get_object_or_404(User, pk=user_id)
    ratings = Rating.objects.all().filter(ratee=user)
    paginator = Paginator(ratings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/ratings.html', {
        'user': get_object_or_404(User, pk=user_id),
        'user_profile': get_object_or_404(UserProfile.objects.select_related(), user_id=user_id),
        'page_obj': page_obj
    })


@login_required
def send_message(request, to_user_id=''):
    """This view lets a user send a message to another user."""
    if request.method == 'POST':
        form = MessageCreateForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = get_object_or_404(User, pk=request.user.id)
            message.seen = False
            message.recipient = get_object_or_404(User, username=request.POST['to'])
            message.sent = datetime.datetime.now()
            message.save()
            messages.success(request, 'Message sent!')
            return get_message_chain(request, message.recipient.id)
        else:
            messages.error(request, 'Message could not be sent')
    else:
        to_user = get_object_or_404(User, pk=to_user_id)
        form = MessageCreateForm(initial={'to': to_user.username})
        return render(request, 'user/send_message.html', {
            'form': form
        })


@login_required
def get_message_by_id(request, message_id):
    """This view lets a user see a message with the given message_id."""
    message = get_object_or_404(Message, pk=message_id)
    if request.user == message.recipient:
        message.seen = True
        message.save()
    elif request.user != message.sender:
        message.error(request, 'You do not have permission to view that message')
        return redirect('user-profile')
    return render(request, 'user/single_message.html', {
        'message': message})


@login_required
def get_message_chain(request, user_id):
    """This view lets a user see all messages between themselves and another user."""
    all_messages_in_chain = Message.objects.all().filter(
        Q(sender_id=request.user.id, recipient_id=user_id) |
        Q(recipient_id=request.user.id, sender_id=user_id)
    ).order_by('-sent')
    paginator = Paginator(all_messages_in_chain, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    all_messages_in_chain.filter(recipient=request.user).update(seen=True)
    return render(request, 'user/message_chain.html', {
        'page_obj': page_obj,
        'user': get_object_or_404(User, pk=user_id)})


@login_required
def get_user_message_chains(request):
    """This view lets a user see all of their messages, organized by message chain.
    A message chain is all messages between two users."""
    sent_messages = Message.objects.all().filter(sender_id=request.user.id)
    received_messages = Message.objects.all().filter(recipient_id=request.user.id)
    messages = sent_messages.union(received_messages)
    message_chain_partners = []

    for message in messages: # Getting all messages the current user has sent or recieved.
        if message.sender == request.user:
            message_chain_partners.append(message.recipient)
        else:
            message_chain_partners.append(message.sender)

    # Finding a distinct list of users that have sent or received messages from the current user.:
    message_chain_partners = list(set(message_chain_partners))
    message_chains = []

    #For each message chain, we order the messages by time sent.
    for chain in message_chain_partners:
        chain_message = Message.objects.all().filter(
            Q(sender_id=request.user.id, recipient_id=chain.id) |
            Q(recipient_id=request.user.id, sender_id=chain.id)
            ).order_by('-sent').first()
        message_chains.append([chain, chain_message])

    message_chains = sorted(message_chains, key=lambda x: x[1].sent, reverse=True)
    paginator = Paginator(message_chains, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user/messages.html', {
        'page_obj': page_obj,
        'user': request.user})

@login_required
def get_notification_by_id(request, notification_id):
    """This view let's the user see details for a specific notification."""
    notification = get_object_or_404(Notification, pk=notification_id)
    notification.seen = True
    notification.save()
    return render(request, 'user/notification_details.html', {
        'notification': notification})

@login_required
def get_user_notifications(request):
    """This view lets a user see all of their notifications."""
    notifications = Notification.objects.all().filter(recipient_id=request.user.id).order_by('-sent')
    paginator = Paginator(notifications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/user_notifications.html', {
        'page_obj': page_obj,
        'user': get_object_or_404(User, pk=request.user.id)})

