from django.forms import ModelForm, widgets
from checkout.models import PaymentInfo

class PaymentInfoCreateForm(ModelForm):
    class Meta:
        model = PaymentInfo
        exclude = ['id', 'user']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'card_number': widgets.TextInput(attrs={'class': 'form-control'}),
            'expiration_date': widgets.TextInput(attrs={'class': 'form-control'}),
            'cvc': widgets.NumberInput(attrs={'class': 'form-control'})
        }

class PaymentInfoUpdateForm(ModelForm):
    class Meta:
        model = PaymentInfo
        exclude = ['id', 'user']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'card_number': widgets.TextInput(attrs={'class': 'form-control'}),
            'expiration_date': widgets.TextInput(attrs={'class': 'form-control'}),
            'cvc': widgets.NumberInput(attrs={'class': 'form-control'})
        }
