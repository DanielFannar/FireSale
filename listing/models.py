from django.db import models
from django.contrib.auth.models import User


class Listing(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.IntegerField()
    listed = models.DateTimeField()
    available = models.BooleanField()


class ListingImage(models.Model):
    image = models.CharField(max_length=9999)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
