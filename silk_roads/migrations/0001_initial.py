# Generated by Django 4.2.4 on 2023-10-08 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import silk_roads.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='custom_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('race', models.CharField(choices=[('Dark Elf', 'Dark Elf'), ('Dragonborn', 'Dragonborn'), ('Dwarf', 'Dwarf'), ('Elf', 'Elf'), ('Fairy', 'Fairy'), ('Gnome', 'Gnome'), ('Goblin', 'Goblin'), ('Goliath', 'Goliath'), ('Human', 'Human'), ('Orc', 'Orc')], max_length=20)),
                ('Class', models.CharField(choices=[('Barbarian', 'Barbarian'), ('Cleric', 'Cleric'), ('Druid', 'Druid'), ('Fighter', 'Fighter'), ('Monk', 'Monk'), ('Paladin', 'Paladin'), ('Ranger', 'Ranger'), ('Sorcerer', 'Sorcerer'), ('Warlock', 'Warlock'), ('Wizard', 'Wizard')], max_length=20)),
                ('weapon', models.CharField(max_length=100)),
                ('type_story', models.CharField(choices=[('Adventure', 'Adventure')], max_length=25)),
                ('role', models.CharField(choices=[('Villain', 'Villain'), ('Hero', 'Hero'), ('Explorer', 'Explorer'), ('Mercenary', 'Mercenary')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1)),
                ('wisdom', models.IntegerField(default=0)),
                ('strength', models.IntegerField(default=0)),
                ('charisma', models.IntegerField(default=0)),
                ('moral_compass', models.IntegerField(default=50)),
                ('health', models.IntegerField(default=100)),
                ('user', models.ForeignKey(default=silk_roads.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
