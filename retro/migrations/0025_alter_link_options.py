# Generated by Django 3.2.19 on 2023-07-03 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retro', '0024_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='link',
            options={'ordering': ['name']},
        ),
    ]
