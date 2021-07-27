from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from GBHsite.data_preparator import sidebar_data, dice_data, stat_data, hero_data, achievements_data
from Profiles.forms import CreateGroupForm, ChangeUsernameForm, ChangePasswordForm, ChangeEmailForm, ChangeAvatarForm
from Profiles.models import Group, GroupHasMember


@login_required
def profile(request, name):
    guest = False
    group = None
    if name == 'me' or name == request.user.username:
        user_watching_on = request.user
        group = request.user.profile.group
    else:
        guest = True
        user_watching_on = User.objects.get(username=name)
    data = {}
    data.update(sidebar_data(user_watching_on, guest))
    data.update(dice_data(user_watching_on))
    data.update(stat_data(user_watching_on))
    data.update(hero_data(user_watching_on))
    data.update(achievements_data(user_watching_on))
    data.update({'group': group})
    return render(request, 'profiles_pages/profile/main.html', data)


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
    data.update(sidebar_data(request.user, False))
    data.update({'group': request.user.profile.group})
    return render(request, 'profiles_pages/profile/settings/main.html', data)


def redirect_success(request, action):
    data = {'username_form': ChangeUsernameForm(user=request.user),
            'password_form': ChangePasswordForm(user=request.user),
            'email_form': ChangeEmailForm(user=request.user),
            'avatar_form': ChangeAvatarForm(),
            action: True}
    data.update(sidebar_data(request.user, False))
    return render(request, 'profiles_pages/profile/settings/main.html', data)


def create_group(request):
    if request.user.profile.group:
        return redirect('/profile/me')
    data = {}
    data.update(sidebar_data(request.user, False))
    create_group_form = CreateGroupForm(user=request.user, data=request.POST or None)
    if request.method == 'POST':
        create_group_form = CreateGroupForm(user=request.user, data=request.POST or None)
        if create_group_form.is_valid():
            new_group = Group.objects.create(
                name=create_group_form.cleaned_data.get('title'),
                leader=request.user,
                private=create_group_form.cleaned_data.get('private'),
                min_level=create_group_form.cleaned_data.get('min_level'))
            member_ = GroupHasMember.objects.create(
                group=new_group,
                member=request.user,
                role=create_group_form.cleaned_data.get('role'),
                hero=None
            )
            new_group.grouphasmember_set.add(member_)
            new_group.save()
            request.user.profile.group = new_group
            request.user.save()
            return redirect('/profile/me')

    data.update({'create_group_form': create_group_form})
    return render(request, 'profiles_pages/create_group/main.html', data)


def inspect_hero(request, user_name, hero_set_id):
    user = User.objects.get(username=user_name)
    data = {}
    hero_set = user.profile.profilehashero_set.get(id=hero_set_id)
    weapon = hero_set.equipment_weapon
    body = hero_set.equipment_body
    trinket1 = hero_set.equipment_trinket1
    trinket2 = hero_set.equipment_trinket2
    total_health = hero_set.hero.base_health
    total_defense = hero_set.hero.base_defense
    total_mana = hero_set.hero.base_mana
    total_armor = hero_set.hero.base_armor
    spell_power = 0
    attack_power = 0
    equipment = [weapon, body, trinket1, trinket2]
    for i in equipment:
        if i:
            total_health += i.health
            total_defense += i.defense
            total_mana += i.mana
            total_armor += i.armor
            spell_power += i.spell
            attack_power += i.attack
    armor_type = hero_set.hero.armor_type

    data.update({'username': user.username,
                 'hero': hero_set,
                 'total_defense': total_defense,
                 'total_armor': total_armor,
                 'total_mana': total_mana,
                 'total_health': total_health,
                 'spell_power': spell_power,
                 'attack_power': attack_power,
                 'armor_type': armor_type,
                 'weapon': weapon,
                 'body': body,
                 'trinket1': trinket1,
                 'trinket2': trinket2})
    return render(request, 'profiles_pages/inspect_hero/hero.html', data)
