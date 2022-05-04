from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from user.forms.profile_form import ProfileForm
from user.models import UserProfile
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    return render(request, 'user/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'user/register.html', {
        'form': UserCreationForm()
    })

def profile(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    if request == 'POST':
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('')
    return render(request, 'user/profile.html',{
        'form': ProfileForm(instance=profile)
    })