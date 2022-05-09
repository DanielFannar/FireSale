from django.forms import ModelForm, widgets

from user.models import Message


class MessageCreateForm(ModelForm):
    class Meta:
        model = Message
        exclude = ['id', 'sender', 'seen', 'sent']
        widgets = {
            'recipient': widgets.TextInput(attrs={'class': 'form-control'}),
            'content': widgets.TextInput(attrs={'class': 'form-control'})
        }
