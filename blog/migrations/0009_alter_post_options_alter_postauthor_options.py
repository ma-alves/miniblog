# Generated by Django 4.2.4 on 2023-11-12 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_postauthor_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': (('can_update', 'Update post content.'),)},
        ),
        migrations.AlterModelOptions(
            name='postauthor',
            options={},
        ),
    ]