from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User


ROLES = (
    ('dps', 'DPS'),
    ('healer', 'Healer'),
    ('tank', 'tank')
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    experience = models.IntegerField(null=False, blank=False, default=0)
    ardor = models.IntegerField(null=False, blank=False, default=0)
    money = models.BigIntegerField(null=False, blank=False, default=0)
    heroes = models.ManyToManyField('GameObjects.Hero', through='ProfileHasHero', null=True)
    achievements = models.ManyToManyField('GameObjects.Achievement', through='ProfileHasAchievement')
    dice = models.ManyToManyField('GameObjects.Dice', through='ProfileHasDice')
    avatar = models.CharField(null=True, blank=True, default=None, max_length=200)
    group = models.ForeignKey('Group', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)


class Statistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    solo = models.OneToOneField('SoloData', on_delete=models.CASCADE, null=True)
    group = models.OneToOneField('GroupData', on_delete=models.CASCADE, null=True)
    total_hours_played = models.BigIntegerField(default=0, null=False, blank=False)
    total_ardor_points = models.BigIntegerField(default=0, null=False, blank=False)
    dice_rolled = models.BigIntegerField(default=0, null=False, blank=False)


class SoloData(models.Model):
    statistics_link = models.OneToOneField(Statistics, on_delete=models.CASCADE)
    games_played = models.IntegerField(default=0, null=False, blank=False)
    floors_passed = models.BigIntegerField(default=0, null=False, blank=False)
    monsters_killed = models.BigIntegerField(default=0, null=False, blank=False)
    max_floor_normal = models.IntegerField(default=0, null=False, blank=False)
    max_floor_chaos = models.IntegerField(default=0, null=False, blank=False)


class GroupData(models.Model):
    statistics_link = models.OneToOneField(Statistics, on_delete=models.CASCADE)
    games_played = models.IntegerField(default=0, null=False, blank=False)
    floors_passed = models.BigIntegerField(default=0, null=False, blank=False)
    monsters_killed = models.BigIntegerField(default=0, null=False, blank=False)
    max_floor_normal = models.IntegerField(default=0, null=False, blank=False)
    max_floor_chaos = models.IntegerField(default=0, null=False, blank=False)
    total_damage_healed = models.IntegerField(default=0, null=False, blank=False)
    total_damage_absorbed = models.IntegerField(default=0, null=False, blank=False)


class ProfileHasHero(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    hero = models.ForeignKey('GameObjects.Hero', null=True, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    date_obtained = models.DateField(null=False, blank=False)
    times_played = models.IntegerField(default=0, editable=False)
    group_played = models.IntegerField(default=0)
    solo_played = models.IntegerField(default=0)
    equipment_weapon = models.ForeignKey('GameObjects.Equipment', on_delete=models.SET_NULL,
                                         related_name='%(class)s_weapon', blank=True, null=True)
    equipment_body = models.ForeignKey('GameObjects.Equipment', on_delete=models.SET_NULL,
                                       related_name='%(class)s_body', blank=True, null=True)
    equipment_trinket1 = models.ForeignKey('GameObjects.Equipment', on_delete=models.SET_NULL,
                                           related_name='%(class)s_trinket1', blank=True, null=True)
    equipment_trinket2 = models.ForeignKey('GameObjects.Equipment', on_delete=models.SET_NULL,
                                           related_name='%(class)s_trinket2', blank=True, null=True)
    # chosen_abilities


class ProfileHasAchievement(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
    achievement = models.ForeignKey('GameObjects.Achievement', on_delete=models.DO_NOTHING)
    date_obtained = models.DateField(null=False, blank=False)


class ProfileHasDice(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
    dice = models.ForeignKey('GameObjects.Dice', on_delete=models.DO_NOTHING)
    date_obtained = models.DateField(null=False, blank=False)
    times_played = models.IntegerField(default=0)
    times_rolled = models.IntegerField(default=0)
    combo_procs = models.IntegerField(default=0)
    effect_procs = models.IntegerField(default=0)
    level = models.IntegerField(default=1)


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


class Group(models.Model):
    leader = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_leader')
    name = models.CharField(null=False, blank=False, default='New party', max_length=50)
    date_created = models.DateField(null=False, blank=False, auto_now_add=True)
    members = models.ManyToManyField(User, through='GroupHasMember')
    private = models.BooleanField(null=False, default=False, blank=False)
    min_level = models.IntegerField(null=False, default=1, blank=False)


class GroupHasMember(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateField(null=False, blank=False, auto_now_add=True)
    role = models.CharField(null=False, blank=False, default=ROLES[0], choices=ROLES, max_length=10)
    hero = models.ForeignKey('ProfileHasHero', on_delete=models.DO_NOTHING, null=True, blank=True)


class MembersInline(admin.TabularInline):
    model = GroupHasMember
    extra = 1


class MembersAdmin(admin.ModelAdmin):
    inlines = (MembersInline,)
