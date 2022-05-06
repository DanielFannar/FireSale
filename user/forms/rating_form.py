from django.forms import ModelForm, widgets

from user.models import Rating


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
