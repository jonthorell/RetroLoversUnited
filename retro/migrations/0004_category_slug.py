# Generated by Django 3.2.19 on 2023-06-13 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retro', '0003_auto_20230610_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
