from django.contrib import admin
from database import models

admin.site.register(models.Statistics)
admin.site.register(models.SoloData)
admin.site.register(models.GroupData)

admin.site.register(models.Hero)
admin.site.register(models.Achievement)
admin.site.register(models.Dice)
admin.site.register(models.Equipment)

admin.site.register(models.ProfileHasHero)
admin.site.register(models.ProfileHasAchievement)
admin.site.register(models.ProfileHasDice)

admin.site.register(models.Profile, models.ProfileAdmin)
