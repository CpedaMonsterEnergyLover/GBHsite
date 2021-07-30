from django.db import models


class Dice(models.Model):
    string_id = models.CharField(null=False, blank=False, max_length=64, unique=True)
    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.CharField(null=False, blank=False, max_length=500, default='no description')
    avatar = models.CharField(null=False, blank=False, max_length=200)


class Achievement(models.Model):
    string_id = models.CharField(null=False, blank=False, max_length=64, unique=True)
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
    string_id = models.CharField(null=False, blank=False, max_length=64, unique=True)
    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.CharField(null=False, blank=True, max_length=500, default='no description')
    avatar = models.CharField(null=True, blank=True, max_length=200)
    level = models.IntegerField(default=1, blank=False)
    health = models.IntegerField(null=False, default=0)
    defense = models.IntegerField(null=False, default=0)
    mana = models.IntegerField(null=False, default=0)
    armor = models.IntegerField(null=False, default=0)
    attack = models.IntegerField(null=False, default=0)
    spell = models.IntegerField(null=False, default=0)
    EQUIPMENT_TYPES = (
        (1, 'weapon'),
        (2, 'body'),
        (3, 'trinket'),
        (None, 'None')
    )
    slot = models.IntegerField(blank=True, null=True, choices=EQUIPMENT_TYPES)


class Hero(models.Model):
    string_id = models.CharField(null=False, blank=False, max_length=64, unique=True)
    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.CharField(null=False, blank=False, max_length=500, default='no description')
    base_health = models.IntegerField(null=False, default=1)
    base_defense = models.IntegerField(null=False, default=1)
    base_mana = models.IntegerField(null=False, default=1)
    base_armor = models.IntegerField(null=False, default=0)

    avatar = models.CharField(null=True, blank=True, max_length=200)
    ROLE_TYPES = (
        (1, 'dps'),
        (2, 'healer'),
        (3, 'tank')
    )
    role = models.IntegerField(blank=False, null=False, default=1, choices=ROLE_TYPES)
    ARMOR_TYPES = (
        ('L', 'light'),
        ('M', 'Medium'),
        ('H', 'heavy')
    )
    armor_type = models.CharField(blank=False, null=False, default=ARMOR_TYPES[0], choices=ARMOR_TYPES, max_length=2)
    # Abilities
    # stat_set


