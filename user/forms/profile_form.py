from django.forms import ModelForm, widgets

from user.models import UserProfile, Rating


class CreateProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['id', 'user', 'settings']
        widgets = {
            'bio': widgets.TextInput(attrs={'class': 'form-control'}),
            'profile-image': widgets.TextInput(attrs={'class': 'form-control'})
        }


class UpdateProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['id', 'user', 'settings']
        widgets = {
            'bio': widgets.TextInput(attrs={'class': 'form-control'}),
            'profile-image': widgets.TextInput(attrs={'class': 'form-control'})
        }


class CreateRatingForm(ModelForm):
    class Meta:
        model = Rating
        exclude = ['id', 'rater', 'ratee', 'purchase']
        widgets = {
            'rating': widgets.NumberInput(attrs={'class': 'form-control'}),
            'comment': widgets.TextInput(attrs={'class': 'form-control'})
        }


class UpdateRatingForm(ModelForm):
    class Meta:
        model = Rating
        exclude = ['id', 'rater', 'ratee', 'purchase']
        widgets = {
            'rating': widgets.NumberInput(attrs={'class': 'form-control'}),
            'comment': widgets.TextInput(attrs={'class': 'form-control'})
        }