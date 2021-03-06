# Generated by Django 4.0.4 on 2022-05-09 14:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checkout', '0005_merge_20220506_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactinfo',
            name='user',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentinfo',
            name='user',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='country',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='checkout.country'),
        ),
        migrations.AlterField(
            model_name='contactinfo',
            name='house_number',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='paymentinfo',
            name='cvc',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(999)], verbose_name='CVC'),
        ),
        migrations.AlterField(
            model_name='paymentinfo',
            name='expiration_date',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator(message='Incorrect date format', regex='^(0[1-9]|1[0-2])\\/?([0-9]{2})$')]),
        ),
    ]
