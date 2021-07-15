from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=16, min_length=3, initial='')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password_confirm = forms.CharField(label='Confirm password', widget=forms.PasswordInput())
    email = forms.EmailField(label='Email', initial='')
    birthday = forms.CharField(label='Date of birth', initial='', widget=forms.SelectDateWidget())

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        # password_validation.validate_password(password)
        confirm_password = cleaned_data.get("password_confirm")
        if password != confirm_password:
            raise forms.ValidationError(
                "Password and confirm password does not match"
            )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control bg-light'})
        self.fields['password'].widget.attrs.update({'class': 'form-control bg-light'})
        self.fields['password_confirm'].widget.attrs.update({'class': 'form-control bg-light'})
        self.fields['email'].widget.attrs.update({'class': 'form-control bg-light'})
        self.fields['birthday'].widget.attrs.update({'class': 'form-control bg-light'})


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control bg-light'})
        self.fields['password'].widget.attrs.update({'class': 'form-control bg-light'})
