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


class OfferUpdateForm(ModelForm):
    class Meta:
        model = Offer
        exclude = ['id', 'listing', 'buyer', 'placed', 'accepted']
        widgets = {
            'amount': widgets.NumberInput(attrs={'class': 'form-control'})
        }