# Generated by Django 5.2.3 on 2025-07-08 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_rename_like_post_likecount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='body',
            new_name='postcontent',
        ),
    ]
