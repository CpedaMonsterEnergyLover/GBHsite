# Generated by Django 3.2.5 on 2021-07-25 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProfilesDB', '0002_auto_20210725_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='min_level',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='group',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
