from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# Create your models here.
from offer.models import Offer


class Country(models.Model):
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.country

class ContactInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default=2)
    city = models.CharField(max_length=255)
    street_name = models.CharField(max_length=255)
    house_number = models.IntegerField(validators=[MinValueValidator(1)])
    postal_code = models.CharField(max_length=255)


class PaymentInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16) # TODO: Find better format for CC. Perhaps using regex to validate only digits or storing as bigint leading zeroes in template.
    expiration_date = models.CharField(max_length=5, # TODO: Maybe we should change this to two fields, and have selectinput.
                                        validators=[
                                            RegexValidator(
                                                regex='^(0[1-9]|1[0-2])\/?([0-9]{2})$',
                                                message='Incorrect date format')
                                        ])
    cvc = models.IntegerField(validators=[MaxValueValidator(999)], verbose_name='CVC') # TODO: Change to charfield with digit-only-validation or display leading zeroes in template.


class Purchase(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)
    payment_info = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE)
