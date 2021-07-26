# Generated by Django 3.2.5 on 2021-07-26 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProfilesDB', '0006_auto_20210726_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouphasmember',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProfilesDB.group'),
        ),
        migrations.AlterField(
            model_name='grouphasmember',
            name='hero',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ProfilesDB.profilehashero'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ProfilesDB.group'),
        ),
    ]