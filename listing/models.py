from django.db import models
from django.contrib.auth.models import User


class Condition(models.Model):
    condition_text = models.CharField(max_length=255)

    def __str__(self):
        return self.condition_text


class Listing(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.SET_DEFAULT, default=1)
    listed = models.DateTimeField()
    available = models.BooleanField(default=True)
    purchased = models.BooleanField(default=False)


class ListingImage(models.Model):
    image = models.CharField(max_length=9999)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)



