from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Achievement, Hero, Dice, Equipment
from .object_ids import DICE_IDS, HERO_IDS, ACHIEVEMENT_IDS, EQUIPMENT_IDS


@receiver(post_save, sender=Achievement)
def create_achievement(sender, instance, created, **kwargs):
    if created:
        ACHIEVEMENT_IDS[instance.string_id] = instance.id
        print(ACHIEVEMENT_IDS)


@receiver(post_save, sender=Achievement)
def save_achievement(sender, instance, **kwargs):
    ACHIEVEMENT_IDS[instance.string_id] = instance.id
    print(ACHIEVEMENT_IDS)

