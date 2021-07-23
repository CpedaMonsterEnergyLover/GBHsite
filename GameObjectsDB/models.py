from django.db import models


class Dice(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.CharField(null=False, blank=False, max_length=500, default='no description')
    avatar = models.CharField(null=False, blank=False, max_length=200)


class Achievement(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.CharField(null=False, blank=False, max_length=500, default='no description')
    avatar = models.CharField(null=True, blank=True, max_length=200, default=None)
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
