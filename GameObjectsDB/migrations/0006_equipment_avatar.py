# Generated by Django 3.2.5 on 2021-07-24 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GameObjectsDB', '0005_auto_20210724_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='avatar',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
