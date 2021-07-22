from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    experience = models.IntegerField(null=False, blank=False, default=0)
    ardor = models.IntegerField(null=False, blank=False, default=0)
    money = models.BigIntegerField(null=False, blank=False, default=0)
    heroes = models.ManyToManyField('Hero', through='ProfileHasHero')
    achievements = models.ManyToManyField('Achievement', through='ProfileHasAchievement')
    dice = models.ManyToManyField('Dice', through='ProfileHasDice')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Statistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    solo = models.OneToOneField('SoloData', on_delete=models.CASCADE, null=True)
    group = models.OneToOneField('GroupData', on_delete=models.CASCADE, null=True)
    total_hours_played = models.BigIntegerField(default=0, null=False, blank=False)
    total_ardor_points = models.BigIntegerField(default=0, null=False, blank=False)
    dice_rolled = models.BigIntegerField(default=0, null=False, blank=False)

    @receiver(post_save, sender=User)
    def create_statistic(sender, instance, created, **kwargs):
        if created:
            Statistics.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_statistic(sender, instance, **kwargs):
        instance.statistics.save()


class SoloData(models.Model):
    statistics_link = models.OneToOneField(Statistics, on_delete=models.CASCADE)
    games_played = models.IntegerField(default=0, null=False, blank=False)
    floors_passed = models.BigIntegerField(default=0, null=False, blank=False)
    monsters_killed = models.BigIntegerField(default=0, null=False, blank=False)
    max_floor_normal = models.IntegerField(default=0, null=False, blank=False)
    max_floor_chaos = models.IntegerField(default=0, null=False, blank=False)

    @receiver(post_save, sender=Statistics)
    def create_solo_data(sender, instance, created, **kwargs):
        if created:
            created_data = SoloData.objects.create(statistics_link=instance)
            instance.solo = created_data

    @receiver(post_save, sender=Statistics)
    def save_solo_data(sender, instance, **kwargs):
        instance.solo.save()


class GroupData(models.Model):
    statistics_link = models.OneToOneField(Statistics, on_delete=models.CASCADE)
    games_played = models.IntegerField(default=0, null=False, blank=False)
    floors_passed = models.BigIntegerField(default=0, null=False, blank=False)
    monsters_killed = models.BigIntegerField(default=0, null=False, blank=False)
    max_floor_normal = models.IntegerField(default=0, null=False, blank=False)
    max_floor_chaos = models.IntegerField(default=0, null=False, blank=False)
    total_damage_healed = models.IntegerField(default=0, null=False, blank=False)
    total_damage_absorbed = models.IntegerField(default=0, null=False, blank=False)

    @receiver(post_save, sender=Statistics)
    def create_group_data(sender, instance, created, **kwargs):
        if created:
            created_data = GroupData.objects.create(statistics_link=instance)
            instance.group = created_data

    @receiver(post_save, sender=Statistics)
    def save_group_data(sender, instance, **kwargs):
        instance.group.save()


class Hero(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.CharField(null=False, blank=False, max_length=500, default='no description')
    base_health = models.IntegerField(null=False, default=1)
    base_defense = models.IntegerField(null=False, default=1)
    base_mana = models.IntegerField(null=False, default=1)
    avatar = models.CharField(null=True, blank=True, max_length=200)
    ROLE_TYPES = (
        (1, 'dps'),
        (2, 'healer'),
        (3, 'tank')
    )
    role = models.IntegerField(blank=False, null=False, default=1, choices=ROLE_TYPES)
    # Abilities
    # stat_set


class ProfileHasHero(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
    hero = models.ForeignKey('Hero', on_delete=models.DO_NOTHING)
    # TODO: make unique
    level = models.IntegerField(default=1)
    date_obtained = models.DateField(null=False, blank=False)
    times_played = models.IntegerField(default=0)
    group_played = models.IntegerField(default=0)
    solo_played = models.IntegerField(default=0)
    equipment_weapon = models.ForeignKey('Equipment', on_delete=models.DO_NOTHING,
                                         related_name='%(class)s_weapon', blank=True, null=True)
    equipment_body = models.ForeignKey('Equipment', on_delete=models.DO_NOTHING,
                                       related_name='%(class)s_body', blank=True, null=True)
    equipment_trinket1 = models.ForeignKey('Equipment', on_delete=models.DO_NOTHING,
                                           related_name='%(class)s_trinket1', blank=True, null=True)
    equipment_trinket2 = models.ForeignKey('Equipment', on_delete=models.DO_NOTHING,
                                           related_name='%(class)s_trinket2', blank=True, null=True)
    # chosen_abilities


class ProfileHasAchievement(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
    achievement = models.ForeignKey('Achievement', on_delete=models.DO_NOTHING)
    date_obtained = models.DateField(null=False, blank=False)


class Achievement(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.CharField(null=False, blank=False, max_length=500, default='no description')
    avatar = models.CharField(null=False, blank=False, max_length=200)
    RARITY = (
        (1, 'Common'),
        (2, 'Uncommon'),
        (3, 'Rare'),
        (4, 'Epic'),
        (5, 'Artifact'),
        (6, 'Mythic'),
    )
    rarity = models.IntegerField(blank=False, null=False, choices=RARITY, default=RARITY[0])
    ARDOR_ = (
        (5, 'Common'),
        (10, 'Uncommon'),
        (15, 'Rare'),
        (25, 'Epic'),
        (50, 'Artifact'),
        (100, 'Mythic'),
    )
    ardor = models.IntegerField(blank=False, null=False, choices=ARDOR_, default=ARDOR_[0])
    rarity_html_tag = models.CharField(null=False, blank=False, max_length=15, default='common')


class Dice(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.CharField(null=False, blank=False, max_length=500, default='no description')


class ProfileHasDice(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
    dice = models.ForeignKey('Dice', on_delete=models.DO_NOTHING)
    date_obtained = models.DateField(null=False, blank=False)
    times_played = models.IntegerField(default=0)
    times_tolled = models.IntegerField(default=0)


class Equipment(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.CharField(null=False, blank=True, max_length=500, default='no description')
    level = models.IntegerField(default=1, blank=False)
    EQUIPMENT_TYPES = (
        (1, 'weapon'),
        (2, 'body'),
        (3, 'trinket'),
        (None, 'None')
    )
    slot = models.IntegerField(blank=True, null=True, choices=EQUIPMENT_TYPES)


class HeroesInline(admin.TabularInline):
    model = ProfileHasHero
    extra = 1


class AchievementsInline(admin.TabularInline):
    model = ProfileHasAchievement
    extra = 1


class DiceInline(admin.TabularInline):
    model = ProfileHasDice
    extra = 1


class ProfileAdmin(admin.ModelAdmin):
    inlines = (HeroesInline, AchievementsInline, DiceInline)
