from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Listing(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.IntegerField()
    listed = models.DateTimeField()
    available = models.BooleanField()
