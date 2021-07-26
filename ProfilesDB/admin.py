from django.contrib import admin
from ProfilesDB import models
from GameObjectsDB import models as game_object_models

admin.site.register(models.Statistics)
admin.site.register(models.SoloData)
admin.site.register(models.GroupData)

admin.site.register(game_object_models.Hero)
admin.site.register(game_object_models.Achievement)
admin.site.register(game_object_models.Dice)
admin.site.register(game_object_models.Equipment)

admin.site.register(models.ProfileHasHero)
admin.site.register(models.ProfileHasAchievement)
admin.site.register(models.ProfileHasDice)
admin.site.register(models.GroupHasMember)

admin.site.register(models.Profile, models.ProfileAdmin)
admin.site.register(models.Group, models.MembersAdmin)
