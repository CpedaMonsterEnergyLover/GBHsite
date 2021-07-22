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
    # heroes
    heroes = user.profile.profilehashero_set.all()
    heroes_set = heroes.order_by('level').reverse()
    top_solo = heroes_set.exclude(solo_played=0).order_by('solo_played')
    top_group = heroes_set.exclude(group_played=0).order_by('group_played')
    heroes_count = heroes.count()
    more_than_9 = False
    if heroes_count > 0:
        for hero in heroes_set:
            hero.times_played = hero.group_played + hero.solo_played
    if heroes_count > 9:
        more_than_9 = True
    # heroes roles bar
    dps_plays = 0
    for i in top_group.filter(hero__role=1):
        dps_plays += i.group_played
    healer_plays = 0
    for i in top_group.filter(hero__role=2):
        healer_plays += i.group_played
    tank_plays = 0
    for i in top_group.filter(hero__role=3):
        tank_plays += i.group_played
    group_plays_count = healer_plays + dps_plays + tank_plays
    dps_percent = 0
    healer_percent = 0
    tank_percent = 0
    if group_plays_count != 0:
        dps_percent = int(round(dps_plays / group_plays_count * 100))
        healer_percent = int(round(healer_plays / group_plays_count * 100))
        tank_percent = int(round(tank_plays / group_plays_count * 100))
    # Achievements
    achievements = user.profile.profilehasachievement_set.all().order_by('achievement__rarity').reverse()
    achievements_count = achievements.count()
    for i in achievements:
        rarity = i.achievement.rarity
        rarity_tag = ['common', 'uncommon', 'rare', 'epic', 'artifact', 'mythic']
        i.achievement.rarity_html_tag = rarity_tag[rarity - 1]
    # Render
    return render(request, 'sitepages/profile/main.html', {
        'level': level,
        'exp': left_exp,
        'percent': percent,
        'solo_games': solo_games,
        'group_games': group_plays_count,
        'max_level': max_level,
        'solo_percent': solo_percent,
        'group_percent': group_percent,
        'total_games': total_games,
        'heroes': heroes_set[:9],
        'heroes_count': heroes_count,
        'top_solo': top_solo[:5],
        'top_group': top_group[:5],
        'more_than_9': more_than_9,
        'dps_percent': dps_percent,
        'healer_percent': healer_percent,
        'tank_percent': tank_percent,
        'achievements': achievements,
        'achievements_count': achievements_count
    })


@login_required
def logout_user(request):
    logout(request)
    return redirect('/')
