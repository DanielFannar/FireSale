from django.forms import ModelForm, widgets

from user.models import UserProfile


class CreateProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['id', 'user', 'settings']
        widgets = {
            'bio': widgets.TimeInput(attrs={'class': 'form-control'}),
            'profile-image': widgets.TextInput(attrs={'class': 'form-control'})
        }
