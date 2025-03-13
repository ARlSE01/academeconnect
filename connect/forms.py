from django import forms
from .models import *

class UserForm(forms.Form):
    # Username = forms.CharField(max_length=200)
    # Email = forms.EmailField(max_length=50)
    # Password = forms.CharField(widget=forms.PasswordInput())
    Email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full p-3 rounded-lg bg-white/20 text-black placeholder-gray-300 shadow-md focus:ring-2 focus:ring-teal-400 outline-none'
    }))
    Username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 rounded-lg bg-white/20 text-black placeholder-gray-300 shadow-md focus:ring-2 focus:ring-teal-400 outline-none'
    }))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full p-3 rounded-lg bg-white/20 text-black placeholder-gray-300 shadow-md focus:ring-2 focus:ring-teal-400 outline-none'
    }))
    # Tags = forms.MultipleChoiceField(
    #     choices=[('html', 'HTML'), ('css', 'CSS'), ('javascript', 'JavaScript')],
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True
    # )

class TagForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tags.objects.all(),  # Empty initially
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    # class Meta:
    #     model = Tags
    #     fields = ['name']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

