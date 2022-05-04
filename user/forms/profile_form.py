from django.forms import ModelForm, widgets

from user.models import UserProfile


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['id', 'user']
        widgets = {
            'bio': widgets.TextInput(attrs={'class': 'form-control'}),
            'profile-image': widgets.TextInput(attrs={'class': 'form-control'})
        }