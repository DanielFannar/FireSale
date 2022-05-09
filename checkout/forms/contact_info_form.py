from django.forms import ModelForm, widgets
from checkout.models import ContactInfo

class ContactInfoCreateForm(ModelForm):
    class Meta:
        model = ContactInfo
        exclude = ['id', 'user']
        widgets = {
            'full_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'country': widgets.Select(attrs={'class': 'form-control'}),
            'city': widgets.TextInput(attrs={'class': 'form-control'}),
            'street_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'house_number': widgets.NumberInput(attrs={'class': 'form-control'}),
            'postal_code': widgets.TextInput(attrs={'class': 'form-control'})
        }


class ContactInfoUpdateForm(ModelForm):
    class Meta:
        model = ContactInfo
        exclude = ['id', 'user']
        widgets = {
            'full_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'country': widgets.Select(attrs={'class': 'form-control'}),
            'city': widgets.TextInput(attrs={'class': 'form-control'}),
            'street_name': widgets.TextInput(attrs={'class': 'form-control'}),
            'house_number': widgets.NumberInput(attrs={'class': 'form-control'}),
            'postal_code': widgets.TextInput(attrs={'class': 'form-control'})
        }
