# Generated by Django 4.0.4 on 2022-05-11 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0003_alter_listing_condition'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='purchased',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='listing',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
