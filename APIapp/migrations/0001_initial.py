# Generated by Django 3.2.5 on 2021-07-12 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LocationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('game_id', models.IntegerField(verbose_name='Игровой айди')),
            ],
        ),
        migrations.CreateModel(
            name='Monster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('game_id', models.IntegerField(verbose_name='Игровой айди')),
                ('level', models.IntegerField(verbose_name='Уровень')),
                ('dice_id', models.IntegerField(verbose_name='Айди кубиков')),
                ('health', models.IntegerField(verbose_name='Макс. здоровье')),
                ('attack', models.IntegerField(verbose_name='Кол-во кубиков атаки')),
                ('defense', models.IntegerField(verbose_name='Кол-во кубиков защиты')),
                ('rotation_type', models.IntegerField(choices=[(1, 'Бродящий'), (2, 'Патрулирующий'), (3, 'Быстрый')], verbose_name='Тип движения')),
                ('rotation_locations', models.ManyToManyField(to='APIapp.LocationType', verbose_name='Типы локаций')),
            ],
        ),
    ]