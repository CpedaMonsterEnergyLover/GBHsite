from django.contrib import admin
from database import models

admin.site.register(models.Profile)
admin.site.register(models.Statistics)
admin.site.register(models.SoloData)
admin.site.register(models.GroupData)
