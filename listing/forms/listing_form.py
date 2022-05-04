from django.forms import ModelForm, widgets
from django import forms
from listing.models import Listing

CONDITION_CHOICES= [
    ('1', 'Heavily used'),
    ('2', 'Used'),
    ('3', 'New')
    ]


class ListingCreateForm(ModelForm):
    image = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Listing
        exclude = ['id', 'seller', 'listed', 'available']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'condition': widgets.Select(attrs={'class': 'form-control'}, choices=CONDITION_CHOICES),
        }
