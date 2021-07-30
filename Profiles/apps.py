from django.apps import AppConfig
from django.db.models.signals import post_save


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Profiles'

    def ready(self):
        from .models import Statistics
        from django.contrib.auth.models import User
        from .signals import create_group_data, create_solo_data, create_statistic, create_user_profile, save_group_data, save_solo_data, save_statistic, save_user_profile
        post_save.connect(receiver=create_user_profile, sender=User)
        post_save.connect(receiver=save_user_profile, sender=User)
        post_save.connect(receiver=create_statistic, sender=User)
        post_save.connect(receiver=save_statistic, sender=User)
        post_save.connect(receiver=create_solo_data, sender=Statistics)
        post_save.connect(receiver=save_solo_data, sender=Statistics)
        post_save.connect(receiver=create_group_data, sender=Statistics)
        post_save.connect(receiver=save_group_data, sender=Statistics)
