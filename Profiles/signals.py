from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, Statistics, SoloData, GroupData


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def create_statistic(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_statistic(sender, instance, **kwargs):
    instance.statistics.save()


@receiver(post_save, sender=Statistics)
def create_solo_data(sender, instance, created, **kwargs):
    if created:
        created_data = SoloData.objects.create(statistics_link=instance)
        instance.solo = created_data


@receiver(post_save, sender=Statistics)
def save_solo_data(sender, instance, **kwargs):
    instance.solo.save()


@receiver(post_save, sender=Statistics)
def create_group_data(sender, instance, created, **kwargs):
    if created:
        created_data = GroupData.objects.create(statistics_link=instance)
        instance.group = created_data


@receiver(post_save, sender=Statistics)
def save_group_data(sender, instance, **kwargs):
    instance.group.save()
