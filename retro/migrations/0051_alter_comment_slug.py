# Generated by Django 3.2.19 on 2023-08-21 20:23

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retro', '0050_alter_link_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='article.title', unique=True),
        ),
    ]
