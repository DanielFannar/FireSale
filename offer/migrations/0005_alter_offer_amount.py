# Generated by Django 4.0.4 on 2022-05-09 14:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0004_alter_offer_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
