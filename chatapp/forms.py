from django import forms
from django.forms import ModelForm
from .models import *
from connect.models import Tags

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Add message ...', 'class': 'p-4 text-black','autofocus': True }),
        }

class TagForm(forms.Form):
    tags = forms.ModelChoiceField(
        queryset=Tags.objects.all(),  # Empty initially
        widget=forms.RadioSelect(attrs={
            'class': 'text-white',  # Style for the checkbox list
        }),
        required=False
    )