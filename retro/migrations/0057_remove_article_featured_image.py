# Generated by Django 3.2.19 on 2023-08-24 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retro', '0056_alter_comment_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='featured_image',
        ),
    ]