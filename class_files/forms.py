from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password


def is_user_with_that_username(value):
    try:
        user = User.objects.get(username=value)
    except Exception as e:
        user = None
    if user:
        raise ValidationError(_('User with that login already exists!'))


class FileUploadForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), validators=[is_user_with_that_username])
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), validators=[validate_password])
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}), validators=[validate_password])
