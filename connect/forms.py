from django import forms

class UserForm(forms.Form):
    Username = forms.CharField(max_length=200)
    Email = forms.EmailField(max_length=50)
    Password = forms.CharField(widget=forms.PasswordInput())
    Tags = forms.MultipleChoiceField(
        choices=[('html', 'HTML'), ('css', 'CSS'), ('javascript', 'JavaScript')],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
