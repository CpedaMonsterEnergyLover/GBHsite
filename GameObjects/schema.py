import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from GameObjects.models import Dice, Achievement, Equipment, Hero


class DiceType(DjangoObjectType):
    class Meta:
        model = Dice
        fields = ("id", "name", "description", "avatar")


class AchievementType(DjangoObjectType):
    class Meta:
        model = Achievement
        fields = ("id", "description", "avatar", "rarity", "ardor")


class EquipmentType(DjangoObjectType):
    class Meta:
        model = Equipment
        fields = ("id", "name", "description", "avatar", "level",
                  "health", "defense", "mana", "armor", "attack",
                  "spell", "slot")


class HeroType(DjangoObjectType):
    class Meta:
        model = Hero
        fields = ("id", "name", "base_health", "base_defense",
                  "base_mana", "base_armor", "avatar", "role",
                  "armor_type")


class GameObjectsQuery(graphene.ObjectType):
    all_dice = graphene.List(DiceType)
    dice_by_id = graphene.Field(DiceType, id=graphene.Int(required=True))

    def resolve_all_dice(self, info):
        return Dice.objects.all()

    def resolve_dice_by_id(self, info, id):
        try:
            return Dice.objects.get(id=id)
        except Dice.DoesNotExist:
            return None
