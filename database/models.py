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

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()