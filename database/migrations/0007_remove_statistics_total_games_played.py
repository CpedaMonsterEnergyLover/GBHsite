# Generated by Django 3.2.5 on 2021-07-21 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_auto_20210722_0210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statistics',
            name='total_games_played',
        ),
    ]
