from django import forms
from .models import *

class UserForm(forms.Form):
    Username = forms.CharField(max_length=200)
    Email = forms.EmailField(max_length=50)
    Password = forms.CharField(widget=forms.PasswordInput())
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

