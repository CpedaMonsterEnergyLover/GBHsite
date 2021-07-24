# Generated by Django 3.2.5 on 2021-07-24 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameObjectsDB', '0004_hero_base_armor'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='armor',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='equipment',
            name='attack',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='equipment',
            name='defense',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='equipment',
            name='health',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='equipment',
            name='mana',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='equipment',
            name='spell',
            field=models.IntegerField(default=0),
        ),
    ]