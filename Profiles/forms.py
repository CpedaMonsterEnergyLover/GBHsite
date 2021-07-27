from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, validate_slug

from GBHsite.utils import valid_url_extension, valid_url_mimetype
from .models import ROLES


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


class CreateGroupForm(forms.Form):
    title = forms.CharField(label='Group title', max_length=50, min_length=3, initial='')
    private = forms.BooleanField(initial=False, required=False)
    min_level = forms.IntegerField(initial=1,
                                   validators=[MaxValueValidator(100), MinValueValidator(1)])
    role = forms.ChoiceField(choices=ROLES)

    def __init__(self, user, data=None):
        self.user = user
        super(CreateGroupForm, self).__init__(data=data)
        self.fields['title'].initial = user.username + "'s group"
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['private'].widget.attrs.update(
            {'class': 'form-check-input border-secondary',
             'style': 'background-color: #353B40;color: #efefef;width:25px;height:25px'})
        self.fields['min_level'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
        self.fields['role'].widget.attrs.update(
            {'class': 'form-control border-secondary', 'style': 'background-color: #353B40;color: #efefef;'})
