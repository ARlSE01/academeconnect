from django import forms
from django.forms import ModelForm
from .models import *
from connect.models import Tags

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        labels = {
            'body': '',  # Removes the default label
        }
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Type a message...', 'class': 'w-full bg-transparent text-black placeholder-gray-400 px-1 py-2 rounded-lg focus:outline-none','autofocus': True }),
        }

class TagForm(forms.Form):
    tags = forms.ModelChoiceField(
        queryset=Tags.objects.all(),  # Empty initially
        widget=forms.RadioSelect(attrs={
            'class': 'text-gray-800',  # Style for the checkbox list
        }),
        required=False
    )