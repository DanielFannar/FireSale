from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class Country(models.Model):
    country = models.CharField(max_length=255)


class ContactInfo(models.Model):
    full_name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1)
    city = models.CharField(max_length=255)
    street_name = models.CharField(max_length=255)
    house_number = models.IntegerField([MinValueValidator(0)])
    postal_code = models.CharField(max_length=255)


class PaymentInfo(models.Model):
    name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=5)
    cvc = models.IntegerField([MaxValueValidator(999)])


class Purchase(models.Model):
    # offer = models.ForeignKey()
    contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)
    payment_info = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE)
