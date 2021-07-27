# Generated by Django 3.2.5 on 2021-07-26 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GameObjects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='New party', max_length=50)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('private', models.BooleanField(default=False)),
                ('min_level', models.IntegerField(default=1)),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='group_leader', to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('experience', models.IntegerField(default=0)),
                ('ardor', models.IntegerField(default=0)),
                ('money', models.BigIntegerField(default=0)),
                ('avatar', models.CharField(blank=True, default=None, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SoloData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games_played', models.IntegerField(default=0)),
                ('floors_passed', models.BigIntegerField(default=0)),
                ('monsters_killed', models.BigIntegerField(default=0)),
                ('max_floor_normal', models.IntegerField(default=0)),
                ('max_floor_chaos', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_hours_played', models.BigIntegerField(default=0)),
                ('total_ardor_points', models.BigIntegerField(default=0)),
                ('dice_rolled', models.BigIntegerField(default=0)),
                ('group', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Profiles.groupdata')),
                ('solo', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Profiles.solodata')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='solodata',
            name='statistics_link',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Profiles.statistics'),
        ),
        migrations.CreateModel(
            name='ProfileHasHero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1)),
                ('date_obtained', models.DateField()),
                ('times_played', models.IntegerField(default=0, editable=False)),
                ('group_played', models.IntegerField(default=0)),
                ('solo_played', models.IntegerField(default=0)),
                ('equipment_body', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profilehashero_body', to='GameObjects.equipment')),
                ('equipment_trinket1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profilehashero_trinket1', to='GameObjects.equipment')),
                ('equipment_trinket2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profilehashero_trinket2', to='GameObjects.equipment')),
                ('equipment_weapon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profilehashero_weapon', to='GameObjects.equipment')),
                ('hero', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='GameObjects.hero')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Profiles.profile')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileHasDice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_obtained', models.DateField()),
                ('times_played', models.IntegerField(default=0)),
                ('times_rolled', models.IntegerField(default=0)),
                ('combo_procs', models.IntegerField(default=0)),
                ('effect_procs', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=1)),
                ('dice', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='GameObjects.dice')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Profiles.profile')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileHasAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_obtained', models.DateField()),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='GameObjects.achievement')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Profiles.profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='achievements',
            field=models.ManyToManyField(through='Profiles.ProfileHasAchievement', to='GameObjects.Achievement'),
        ),
        migrations.AddField(
            model_name='profile',
            name='dice',
            field=models.ManyToManyField(through='Profiles.ProfileHasDice', to='GameObjects.Dice'),
        ),
        migrations.AddField(
            model_name='profile',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Profiles.group'),
        ),
        migrations.AddField(
            model_name='profile',
            name='heroes',
            field=models.ManyToManyField(through='Profiles.ProfileHasHero', to='GameObjects.Hero'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='GroupHasMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('role', models.CharField(choices=[('dps', 'DPS'), ('healer', 'Healer'), ('tank', 'tank')], default=('dps', 'DPS'), max_length=10)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Profiles.group')),
                ('hero', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Profiles.profilehashero')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='groupdata',
            name='statistics_link',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Profiles.statistics'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, through='Profiles.GroupHasMember', to=settings.AUTH_USER_MODEL),
        ),
    ]