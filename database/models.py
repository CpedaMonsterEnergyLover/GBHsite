# from django.db import models
#
#
# class LocationType(models.Model):
#     name = models.CharField(max_length=50, verbose_name="Название")
#     game_id = models.IntegerField(verbose_name="Игровой айди")
#
#
# class Monster(models.Model):
#     name = models.CharField(max_length=50, verbose_name="Название")
#     game_id = models.IntegerField(verbose_name="Игровой айди")
#     level = models.IntegerField(verbose_name="Уровень")
#     dice_id = models.IntegerField(verbose_name="Айди кубиков")
#     health = models.IntegerField(verbose_name="Макс. здоровье")
#     attack = models.IntegerField(verbose_name="Кол-во кубиков атаки")
#     defense = models.IntegerField(verbose_name="Кол-во кубиков защиты")
#     rotation_type = models.IntegerField(verbose_name="Тип движения",
#                                         choices=[
#                                             (1, "Бродящий"),
#                                             (2, "Патрулирующий"),
#                                             (3, "Быстрый")
#                                         ])
#     rotation_locations = models.ManyToManyField(LocationType, verbose_name="Типы локаций")
# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
#
# class User(AbstractUser):
#     email = models.EmailField()
#     date_of_birth = models.DateField()
#     hui = models.CharField(max_length=100)

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    experience = models.IntegerField(null=False, blank=False, default=0)
    ardor = models.IntegerField(null=False, blank=False, default=0)

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

    # @receiver(post_save, sender='database.SoloData')
    # def add_games_played(sender, instance, **kwargs):
    #     stat = Statistics.objects.get(solo=instance)
    #     stat.total_games_played = instance.games_played
    #     stat.save()


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
