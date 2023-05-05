from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        username = User.objects.filter(username=username).exists()
        if username:
            raise ValidationError('This username has been existence')

    def clean_email(self):
        email = self.cleaned_data['email']
        user_email = User.objects.filter(email=email).exists()
        if user_email:
            raise ValidationError('This email has been existence')

    def clean(self):
        cd = super().clean()
        password = cd.get('password')
        confirm_password = cd.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError('your passwords must match')

