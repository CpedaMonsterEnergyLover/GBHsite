from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import *
from django.shortcuts import redirect


def welcome_site(request):
    return render(request, 'sitepages/home/main.html')


def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            # gets form fields
            password = signup_form.cleaned_data['password']
            username = signup_form.cleaned_data['username']
            email = signup_form.cleaned_data['email']
            birthday = signup_form.cleaned_data['birthday']
            # creates a new user
            user = User.objects.create_user(username, email, password)
            user.profile.birth_date = birthday
            user.save()
            # render submit page
            return render(request, "sitepages/signup/submit/main.html", {'username': username, 'email': email})
        else:
            return render(request, 'sitepages/signup/main.html', {'signup_form': signup_form})
    else:
        signup_form = SignUpForm()

    return render(request, 'sitepages/signup/main.html', {'signup_form': signup_form})


def settings(request):
    change_username_form = ChangeUsernameForm(user=request.user)
    change_password_form = ChangePasswordForm(user=request.user)
    change_email_form = ChangeEmailForm(user=request.user)
    if request.method == 'POST':
        if 'submit_password' in request.POST:
            change_password_form = ChangePasswordForm(user=request.user, data=request.POST or None)

        if 'submit_username' in request.POST:
            change_username_form = ChangeUsernameForm(user=request.user, data=request.POST or None)
            if change_username_form.is_valid():
                return render_settings(request, change_username_form, change_password_form, change_email_form,
                                       {'username_changed': True})
            else:
                return render_settings(request, change_username_form, change_password_form, change_email_form, None)

        if 'submit_email' in request.POST:
            change_email_form = ChangeEmailForm(user=request.user, data=request.POST or None)

    return render_settings(request, change_username_form, change_password_form, change_email_form, None)


@login_required
def profile(request):
    return render(request, 'sitepages/profile/main.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('/')


def render_settings(request, uf, pf, ef, arg):
    d = {'username_form': uf, 'password_form': pf, 'email_form': ef}
    if arg is not None:
        d[arg[1]] = arg[2]
    return render(request, 'sitepages/profile/settings/main.html', d)
