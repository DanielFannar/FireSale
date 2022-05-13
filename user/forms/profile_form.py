from django.forms import ModelForm, widgets
from django import forms

from user.models import UserProfile


class ProfileCreateForm(ModelForm):
    email = forms.EmailField(max_length=255)

    class Meta:
        model = UserProfile
        exclude = ['id', 'user', 'settings']
        widgets = {
            'bio': widgets.TextInput(attrs={'class': 'form-control'}),
            'profile-image': widgets.TextInput(attrs={'class': 'form-control'})
        }


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['id', 'user', 'settings']
        widgets = {
            'bio': widgets.TextInput(attrs={'class': 'form-control'}),
            'profile-image': widgets.TextInput(attrs={'class': 'form-control'})
        }


