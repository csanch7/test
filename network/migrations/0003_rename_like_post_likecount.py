# Generated by Django 5.2.3 on 2025-07-08 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='like',
            new_name='likecount',
        ),
    ]
