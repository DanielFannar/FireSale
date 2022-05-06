import datetime

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm

from user.forms.message_form import CreateMessageForm
from user.forms.profile_form import CreateProfileForm, UpdateProfileForm
from user.forms.rating_form import CreateRatingForm
from user.models import UserProfile, Rating, Message
from user import helper_functions


# Create your views here.


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = CreateProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    else:
        return render(request, 'user/register.html', {
            'user_form': UserCreationForm(),
            'profile_form': CreateProfileForm()
        })


def get_profile(request, user_id=None):
    current_user = request.user
    if user_id is None:
        user_id = request.user.id
    return render(request, 'user/profile.html', {
        'current_user': current_user,
        'user': get_object_or_404(User, pk=user_id),
        'user_profile': get_object_or_404(UserProfile.objects.select_related(), user_id=user_id),
        'rating': helper_functions.get_user_rating(user_id)
    })


def edit_profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    user_profile = get_object_or_404(UserProfile.objects.select_related(), user_id=user.id)
    if request.method == 'POST':
        form = UpdateProfileForm(data=request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('my-profile')
    else:
        form = UpdateProfileForm(instance=user_profile)
        return render(request, 'user/edit_profile.html', {
            'form': form
        })


def get_user_ratings(request, user_id):

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


def send_message(request, to_user_id=''):
    if request.method == 'POST':
        form = CreateMessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = get_object_or_404(User, pk=request.user.id)
            message.seen = False
            message.sent = datetime.datetime.now()
            message.save()
            return get_message_chain(request, message.recipient.id)
    else:
        form = CreateMessageForm(initial={'recipient': get_object_or_404(User, pk=to_user_id)})
    return render(request, 'user/send_message.html', {
        'form': form
    })


def get_message_chain(request, user_id):
    messages = Message.objects.all().filter(
        Q(sender_id=request.user.id, recipient_id=user_id) |
        Q(recipient_id=request.user.id,sender_id=user_id)
    ).order_by('-sent')
    paginator = Paginator(messages, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'user/message_chain.html', {
        'page_obj': page_obj,
        'user': get_object_or_404(User, pk=user_id)})


def get_user_message_chains(request):

    messages = Message.objects.all().filter(sender_id=request.user.id)
    messages.union(Message.objects.all().filter(recipient_id=request.user.id))
    message_chain_partners = []

    for message in messages:
        if message.sender == request.user:
            message_chain_partners.append(message.recipient)
        else:
            message_chain_partners.append(message.sender)

    message_chain_partners = list(set(message_chain_partners))
    message_chains = []

    for chain in message_chain_partners:
        chain_message = Message.objects.all().filter(
            Q(sender_id=request.user.id, recipient_id=chain.id) |
            Q(recipient_id=request.user.id,sender_id=chain.id)
            ).order_by('-sent').first()
        message_chains.append([chain, chain_message])

    message_chains = sorted(message_chains, key=lambda x: x[1].sent, reverse=True)
    paginator = Paginator(message_chains, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user/messages.html', {
        'page_obj': page_obj,
        'user': request.user})


