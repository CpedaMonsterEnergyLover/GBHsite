from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .utils import *
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


@login_required
def settings(request):
    change_username_form = ChangeUsernameForm(user=request.user)
    change_password_form = ChangePasswordForm(user=request.user)
    change_email_form = ChangeEmailForm(user=request.user)
    if request.method == 'POST':
        # username form
        if 'submit_username' in request.POST:
            change_username_form = ChangeUsernameForm(user=request.user, data=request.POST or None)
            if change_username_form.is_valid():
                user = User.objects.get(username=request.user.username)
                user.username = change_username_form.cleaned_data.get('username')
                user.save()
                return redirect('settings/redirect-success/username_changed/')

        # password form
        if 'submit_password' in request.POST:
            change_password_form = ChangePasswordForm(user=request.user, data=request.POST or None)
            if change_password_form.is_valid():
                # TODO: send a letter to confirm an email
                user = User.objects.get(username=request.user.username)
                user.set_password(change_password_form.cleaned_data.get('new_password'))
                user.save()
                return render(request, 'sitepages/profile/settings/main.html',
                              {'username_form': change_username_form,
                               'password_form': ChangePasswordForm(user=request.user),
                               'email_form': change_email_form, 'password_changed': True})
        # email form
        if 'submit_email' in request.POST:
            change_email_form = ChangeEmailForm(user=request.user, data=request.POST or None)
            if change_email_form.is_valid():
                # TODO: send a letter to confirm an email
                user = User.objects.get(username=request.user.username)
                user.email = change_email_form.cleaned_data.get('email')
                user.save()
                return render(request, 'sitepages/profile/settings/main.html',
                              {'username_form': change_username_form,
                               'password_form': change_password_form,
                               'email_form': ChangeEmailForm(user=request.user), 'email_changed': True})

    return render(request, 'sitepages/profile/settings/main.html',
                  {'username_form': change_username_form,
                   'password_form': change_password_form,
                   'email_form': change_email_form})


@login_required
def redirect_success(request, action):
    return render(request, 'sitepages/profile/settings/main.html',
                  {'username_form': ChangeUsernameForm(user=request.user),
                   'password_form': ChangePasswordForm(user=request.user),
                   'email_form': ChangeEmailForm(user=request.user),
                   action: True})


@login_required
def profile(request):
    user = request.user
    stat = user.statistics
    exp = request.user.profile.experience
    # level
    level = calc_level(exp)
    max_level = False
    if exp >= 100000:
        level = 100
        max_level = True
    # sidebar exp
    left_exp = calc_left_exp(exp)
    percent = left_exp // 10
    # total games played
    solo_games = stat.solo.games_played
    group_games = stat.group.games_played
    total_games = solo_games + group_games
    solo_percent = 0
    group_percent = 0
    if total_games > 0:
        solo_percent = int(round(solo_games / total_games * 100))
        group_percent = 100 - solo_percent
    return render(request, 'sitepages/profile/main.html', {
        'level': level,
        'exp': left_exp,
        'percent': percent,
        'solo_games': solo_games,
        'group_games': group_games,
        'max_level': max_level,
        'solo_percent': solo_percent,
        'group_percent': group_percent,
        'total_games': total_games,
    })


@login_required
def logout_user(request):
    logout(request)
    return redirect('/')
