# Generated by Django 4.0.4 on 2022-05-06 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_rename_receiver_message_recipient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='seen',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
