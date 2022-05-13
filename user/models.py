from django.db import models
from django.contrib.auth.models import User

from checkout.models import Purchase
from django.core.validators import MaxValueValidator, MinValueValidator




class UserSettings(models.Model):
    email_notification = models.BooleanField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=6969, default='This user has no bio yet.')
    settings = models.ForeignKey(UserSettings, on_delete=models.SET_NULL, null=True)
    image = models.CharField(max_length=9999, null=True, default='/static/images/no.jpg')

    def __str__(self):
        return self.user.username


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="message_recipient")
    content = models.CharField(max_length=9999)
    seen = models.BooleanField()
    sent = models.DateTimeField()



class Rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="rater")
    ratee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratee")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=999)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['purchase'], name='one rating per purchase')
        ]



class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="notification_recipient")
    content = models.CharField(max_length=9999)
    seen = models.BooleanField()
    sent = models.DateTimeField()
    url = models.CharField(max_length=9999)
