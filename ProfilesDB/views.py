from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from GBHsite.data_preparator import sidebar_data
from ProfilesDB.forms import CreateGroupForm
from ProfilesDB.models import Group, GroupHasMember


def categories(request):
    return render(request, 'dbpages/categories/root.html')


def welcome_database(request):
    return render(request, 'dbpages/home/root.html')


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
