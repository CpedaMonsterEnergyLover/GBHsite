# Generated by Django 3.2.5 on 2021-07-24 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GameObjectsDB', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hero',
            name='armor_type',
        ),
        migrations.RemoveField(
            model_name='hero',
            name='role',
        ),
    ]
