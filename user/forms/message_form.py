from django.forms import ModelForm, widgets
from django import forms
from user.models import Message


class MessageCreateForm(ModelForm):
    to = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Message
        exclude = ['id', 'sender', 'seen', 'sent', 'recipient']
        widgets = {
            'content': widgets.TextInput(attrs={'class': 'form-control'})
        }

    field_order = ['to', 'content']