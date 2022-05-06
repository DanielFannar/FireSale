from django.core.validators import MinValueValidator
from django.db import models
from listing.models import Listing
from django.contrib.auth.models import User

# Create your models here.


class Offer(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    placed = models.DateTimeField()
    accepted = models.BooleanField(default=False)
