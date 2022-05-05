from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from user.forms.profile_form import CreateProfileForm, UpdateProfileForm, CreateRatingForm
from user.models import UserProfile, Rating
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
    if user_id is None:
        user_id = request.user.id
    return render(request, 'user/profile.html', {
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

