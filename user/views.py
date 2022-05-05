from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from user.forms.profile_form import CreateProfileForm
from user.models import UserProfile
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


def profile(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    if request == 'POST':
        form = CreateProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('')
    return render(request, 'user/profile.html',{
        'form': CreateProfileForm(instance=profile)
    })