from datetime import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from .utils import *

from django.utils.translation import ugettext as _


class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=14, min_length=3, initial='', validators=[validate_slug])
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label='Confirm password', widget=forms.PasswordInput())
    email = forms.EmailField(label='Email', initial='')
    birthday = forms.CharField(label='Date of birth', initial=datetime.now().strftime("%Y-%m-%d"),
                               widget=forms.SelectDateWidget(
                                   years=range(1922, 2022)))

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        # old_password validation
        password = cleaned_data.get("password")
        # TODO: password_validation.validate_password(password)
        confirm_password = cleaned_data.get("password_confirm")
        if password != confirm_password:
            raise ValidationError({'password': ['Passwords do not match']})
        # date validation
        date = cleaned_data.get("birthday")
        birthday = datetime.strptime(date, "%Y-%m-%d").date()
        if birthday >= datetime.date(datetime.now()):
            raise forms.ValidationError("Enter a valid date of birth")
        # username exists validation
        username = cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': ['This username is already taken']})

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['password_confirm'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['birthday'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=16, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
