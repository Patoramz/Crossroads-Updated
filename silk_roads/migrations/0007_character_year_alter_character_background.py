# Generated by Django 5.0.2 on 2024-05-04 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('silk_roads', '0006_alter_character_ethnicity'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='year',
            field=models.IntegerField(default=2024),
        ),
        migrations.AlterField(
            model_name='character',
            name='background',
            field=models.CharField(default=' ', max_length=200),
        ),
    ]