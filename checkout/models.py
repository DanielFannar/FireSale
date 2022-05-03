from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class ContactInfo(models.Model):
    full_name = models.CharField(max_length=255)
    # country = models.ForeignKey(Country, on_delete= models.CASCADE)
    city = models.CharField(max_length=255)
    street_name = models.CharField(max_length=255)
    house_number = models.IntegerField([MinValueValidator(0)])
    postal_code = models.CharField(max_length=255)

class PaymentInfo(models.Model):
    name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=5)
    cvc = models.IntegerField(max_length=3)


class Purchase(models.Model):
    # offer = models.ForeignKey()
    contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)
    payment_info = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE)

#Purchase
# offer: Offer
# contact_info: ContactInfo
# payment_info: PaymentInfo
# bought: datetime
# ContactInfo PaymentInfo
# full_name: string
# country: Country
# city: string
#                            name: string
#                            card_number: string
#                            expiration_date: date
#                            cvc: int
#                            street_name: string
# house_number: int
# postal_code: string