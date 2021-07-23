from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import *
from django.shortcuts import redirect
from .data_preparator import *


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
            # TODO: after signup redirect to profile page, not render
    else:
        signup_form = SignUpForm()

    return render(request, 'sitepages/signup/main.html', {'signup_form': signup_form})


@login_required
def settings(request):
    change_username_form = ChangeUsernameForm(user=request.user)
    change_password_form = ChangePasswordForm(user=request.user)
    change_email_form = ChangeEmailForm(user=request.user)
    change_avatar_form = ChangeAvatarForm()

    if request.method == 'POST':
        # avatar form
        if 'submit_avatar' in request.POST:
            change_avatar_form = ChangeAvatarForm(request.POST)
            if change_avatar_form.is_valid():
                user = User.objects.get(username=request.user.username)
                user.profile.avatar = change_avatar_form.cleaned_data.get('avatar')
                user.save()
                return redirect('settings/redirect-success/avatar_changed/')

        # username form
        if 'submit_username' in request.POST:
            change_username_form = ChangeUsernameForm(user=request.user, data=request.POST or None)
            if change_username_form.is_valid():
                user = User.objects.get(username=request.user.username)
                user.username = change_username_form.cleaned_data.get('username')
                user.save()
                return redirect('settings/redirect-success/username_changed/')

        # old_password form
        if 'submit_password' in request.POST:
            change_password_form = ChangePasswordForm(user=request.user, data=request.POST or None)
            if change_password_form.is_valid():
                # TODO: send a letter to confirm an email
                user = User.objects.get(username=request.user.username)
                user.set_password(change_password_form.cleaned_data.get('new_password1'))
                user.save()
                return redirect('/login')

        # email form
        if 'submit_email' in request.POST:
            change_email_form = ChangeEmailForm(user=request.user, data=request.POST or None)
            if change_email_form.is_valid():
                # TODO: send a letter to confirm an email
                user = User.objects.get(username=request.user.username)
                user.email = change_email_form.cleaned_data.get('email')
                user.save()
                return redirect('settings/redirect-success/email_changed/')
    data = {'username_form': change_username_form,
            'password_form': change_password_form,
            'email_form': change_email_form,
            'avatar_form': change_avatar_form}
    data.update(sidebar_data(request.user))
    return render(request, 'sitepages/profile/settings/main.html', data)


def redirect_success(request, action):
    data = {'username_form': ChangeUsernameForm(user=request.user),
            'password_form': ChangePasswordForm(user=request.user),
            'email_form': ChangeEmailForm(user=request.user),
            'avatar_form': ChangeAvatarForm(),
            action: True}
    data.update(sidebar_data(request.user))
    return render(request, 'sitepages/profile/settings/main.html', data)


@login_required
def profile(request):
    user = request.user
    data = {}
    data.update(sidebar_data(user))
    data.update(dice_data(user))
    data.update(stat_data(user))
    data.update(hero_data(user))
    data.update(achievements_data(user))
    return render(request, 'sitepages/profile/main.html', data)


@login_required
def logout_user(request):
    logout(request)
    return redirect('/')
