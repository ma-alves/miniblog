# Generated by Django 4.2.4 on 2024-01-15 18:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0011_rename_postauthor_author'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostComment',
            new_name='Comment',
        ),
    ]
