from django.forms import ModelForm, widgets
from django import forms
from offer.models import Offer


class OfferCreateForm(ModelForm):
    class Meta:
        model = Offer
        exclude = ['id', 'listing', 'buyer', 'placed', 'accepted']
        widgets = {
            'amount': widgets.NumberInput(attrs={'class': 'form-control'})
        }

'''
class ListingUpdateForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ['id', 'seller', 'listed', 'available']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.TextInput(attrs={'class': 'form-control'}),
            'condition': widgets.Select(attrs={'class': 'form-control'}, choices=CONDITION_CHOICES)
        }
'''