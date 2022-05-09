from django.forms import ModelForm, widgets

from user.models import UserProfile


class ProfileCreateForm(ModelForm):
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


