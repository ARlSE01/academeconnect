from django import forms
from .models import *

class UserForm(forms.Form):
    Email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full p-3 rounded-lg bg-white/20 text-black placeholder-gray-300 shadow-md focus:ring-2 focus:ring-teal-400 outline-none'
    }))
    Username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full p-3 rounded-lg bg-white/20 text-black placeholder-gray-300 shadow-md focus:ring-2 focus:ring-teal-400 outline-none'
    }))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full p-3 rounded-lg bg-white/20 text-black placeholder-gray-300 shadow-md focus:ring-2 focus:ring-teal-400 outline-none'
    }))


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
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-7 rounded-lg bg-white/100 text-black placeholder:text-white shadow-md focus:ring-2 focus:ring-teal-400 outline-none h-12',
                'placeholder': 'Enter title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-7 rounded-lg bg-white/100 text-black placeholder:text-white shadow-md focus:ring focus:ring-teal-400 outline-none h-30',
                'placeholder': 'Enter content'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full p-2 bg-gray-300 text-black rounded-lg',
                'rows': 1,
                'placeholder': 'Write your comment...',
            }),
        }

