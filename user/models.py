from django.db import models
from django.contrib.auth.models import User
from checkout.models import Purchase
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class UserSettings(models.Model):
    offer_received = models.BinaryField()
    offer_accepted = models.BinaryField()
    offer_declined = models.BinaryField()
    email_notification = models.BinaryField()
    push_notification = models.BinaryField()


class UserProfile(models.Model):
    bio = models.CharField(max_length=6969) # ;)
    settings = models.ForeignKey(UserSettings, on_delete=models.SET_NULL)


class ProfileImage(models.Model):
    image = models.CharField(max_length=9999)
    user = models.OneToOneRel(UserProfile, on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL)
    content = models.CharField(max_length=9999)
    seen = models.BinaryField()
    sent = models.DateTimeField()


class Rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.SET_NULL)
    ratee = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField([MinValueValidator(1)], [MaxValueValidator(5)])
    comment = models.CharField(max_length=999)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)