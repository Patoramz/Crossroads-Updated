# Generated by Django 5.0.2 on 2024-05-12 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('silk_roads', '0007_character_year_alter_character_background'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='background',
            field=models.CharField(default=' ', max_length=250),
        ),
    ]