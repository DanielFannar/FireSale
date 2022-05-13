# Generated by Django 4.0.4 on 2022-05-13 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_remove_usersettings_email_notification_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersettings',
            name='temporary',
        ),
        migrations.AddField(
            model_name='usersettings',
            name='email_notification',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]