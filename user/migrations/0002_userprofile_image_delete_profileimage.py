# Generated by Django 4.0.4 on 2022-05-05 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.CharField(max_length=9999, null=True),
        ),
        migrations.DeleteModel(
            name='ProfileImage',
        ),
    ]
