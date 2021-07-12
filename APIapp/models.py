from django.db import models


class LocationType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    game_id = models.IntegerField(verbose_name="Игровой айди")


class Monster(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    game_id = models.IntegerField(verbose_name="Игровой айди")
    level = models.IntegerField(verbose_name="Уровень")
    dice_id = models.IntegerField(verbose_name="Айди кубиков")
    health = models.IntegerField(verbose_name="Макс. здоровье")
    attack = models.IntegerField(verbose_name="Кол-во кубиков атаки")
    defense = models.IntegerField(verbose_name="Кол-во кубиков защиты")
    rotation_type = models.IntegerField(verbose_name="Тип движения",
                                        choices=[
                                            (1, "Бродящий"),
                                            (2, "Патрулирующий"),
                                            (3, "Быстрый")
                                        ])
    rotation_locations = models.ManyToManyField(LocationType, verbose_name="Типы локаций")
