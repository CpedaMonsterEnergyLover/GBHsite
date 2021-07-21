# Generated by Django 3.2.5 on 2021-07-21 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_auto_20210722_0055'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games_played', models.IntegerField(default=0)),
                ('floors_passed', models.BigIntegerField(default=0)),
                ('monsters_killed', models.BigIntegerField(default=0)),
                ('max_floor_normal', models.IntegerField(default=0)),
                ('max_floor_chaos', models.IntegerField(default=0)),
                ('total_damage_healed', models.IntegerField(default=0)),
                ('total_damage_absorbed', models.IntegerField(default=0)),
                ('statistics_link', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='database.statistics')),
            ],
        ),
        migrations.AddField(
            model_name='statistics',
            name='group',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='database.groupdata'),
        ),
    ]
