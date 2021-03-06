# Generated by Django 4.0.4 on 2022-05-03 18:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='paymentinfo',
            name='cvc',
            field=models.IntegerField(verbose_name=[django.core.validators.MaxValueValidator(999)]),
        ),
        migrations.AddField(
            model_name='contactinfo',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='checkout.country'),
        ),
    ]
