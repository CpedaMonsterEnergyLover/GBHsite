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
        if User.objects.filter(username=cleaned_data['username']).exists():
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


class ChangeUsernameForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    username = forms.CharField(label='Username', max_length=14, min_length=3, initial='', validators=[validate_slug])

    def clean(self):
        cleaned_data = super(ChangeUsernameForm, self).clean()
        # old_password check
        password = cleaned_data.get("password")
        if not self.user.check_password(password):
            raise ValidationError({'password': ['Invalid password']})
        # username exists validation
        username = cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken')

    def __init__(self, user, data=None):
        self.user = user
        super(ChangeUsernameForm, self).__init__(data=data)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Password', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        # old_password check
        password = cleaned_data.get("old_password")
        if not self.user.check_password(password):
            raise ValidationError({'old_password': ['Invalid password']})
        # old_password validation
        # TODO: password_validation.validate_password(old_password)
        new_password = cleaned_data.get("new_password1")
        confirm_password = cleaned_data.get("new_password2")
        if new_password != confirm_password:
            raise ValidationError({'new_password2   ': ['Passwords do not match']})

    def __init__(self, user, data=None):
        self.user = user
        super(ChangePasswordForm, self).__init__(data=data)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})


class ChangeEmailForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    email = forms.EmailField(label='Email', initial='')

    def clean(self):
        cleaned_data = super(ChangeEmailForm, self).clean()
        # old_password check
        password = cleaned_data.get("old_password")
        if not self.user.check_password(password):
            raise ValidationError({'old_password': ['Invalid old_password']})
        # email exists validation
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise ValidationError({'email': ['This email is taken']})

    def __init__(self, user, data=None):
        self.user = user
        super(ChangeEmailForm, self).__init__(data=data)
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})


class ChangeAvatarForm(forms.Form):
    avatar = forms.URLField(label='New image URL', required=True, max_length=200, )

    def clean(self):
        cleaned_data = super(ChangeAvatarForm, self).clean()
        url = cleaned_data.get('avatar')
        if not valid_url_extension(url) or not valid_url_mimetype(url):
            raise ValidationError(
                {'avatar': ['Not a valid Image. The URL must have an image extensions (.jpg/.jpeg/.png)']})

    def __init__(self, *args, **kwargs):
        super(ChangeAvatarForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})

