from .utils import *


def sidebar_data(user, guest):
    exp = user.profile.experience
    # level
    level = calc_level(exp)
    max_level = False
    if exp >= 100000:
        level = 100
        max_level = True
    # sidebar exp
    left_exp = calc_left_exp(exp)
    percent = left_exp // 10
    username = user.username
    registration_date = user.date_joined.date
    email = user.email
    avatar = user.profile.avatar
    if guest:
        email = None
    return {'avatar': avatar,
            'guest': guest,
            'username': username,
            'registration_date': registration_date,
            'email': email,
            'level': level,
            'exp': left_exp,
            'percent': percent,
            'max_level': max_level}


def dice_data(user):
    dice = user.profile.profilehasdice_set.all().order_by('level')
    dice_count = dice.count()
    more_than_9d = 0
    top_dice = dice.exclude(times_played=0).order_by('times_played')
    if dice_count > 9:
        more_than_9d = True
    return {
        'dice_count': dice_count,
        'dice_list': dice,
        'top_dice': top_dice[:5],
        'more_than_9d': more_than_9d
    }


def stat_data(user):
    stat = user.statistics
    solo_games = stat.solo.games_played
    group_games = stat.group.games_played
    total_games = solo_games + group_games
    solo_percent = 0
    group_percent = 0
    if total_games > 0:
        solo_percent = int(round(solo_games / total_games * 100))
        group_percent = 100 - solo_percent
    return {'solo_games': solo_games,
            'solo_percent': solo_percent,
            'group_percent': group_percent,
            'total_games': total_games}


def hero_data(user):
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
    return {'heroes': heroes_set[:9],
            'heroes_count': heroes_count,
            'top_solo': top_solo[:5],
            'top_group': top_group[:5],
            'more_than_9': more_than_9,
            'dps_percent': dps_percent,
            'healer_percent': healer_percent,
            'tank_percent': tank_percent}


def achievements_data(user):
    achievements = user.profile.profilehasachievement_set.all().order_by('achievement__rarity').reverse()
    achievements_count = achievements.count()
    for i in achievements:
        rarity = i.achievement.rarity
        rarity_tag = ['common', 'uncommon', 'rare', 'epic', 'artifact', 'mythic']
        i.achievement.rarity_html_tag = rarity_tag[rarity - 1]
    return {'achievements': achievements,
            'achievements_count': achievements_count}
