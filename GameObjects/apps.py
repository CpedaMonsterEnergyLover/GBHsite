from django.apps import AppConfig
from django.db.models.signals import post_save


class GameobjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GameObjects'

    def ready(self):
        from .models import Achievement
        from .signals import create_achievement, save_achievement
        post_save.connect(receiver=create_achievement, sender=Achievement)
        post_save.connect(receiver=save_achievement, sender=Achievement)
