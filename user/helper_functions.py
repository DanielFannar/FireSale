from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import request
from django.shortcuts import get_object_or_404
from django.utils import timezone

from offer.models import Offer
from user.models import Message, UserProfile, Notification
from user.views import send_notification_mail


def send_notification(user_id, notification_message):
    user = get_object_or_404(User, pk=user_id)
    #user_profile = get_object_or_404(UserProfile, user=user)
    notification = Notification(recipient=user, content=notification_message, seen=False, sent=timezone.now())
    notification.save()
    #if user_profile.settings.email_notification == True:
    send_notification_mail(notification.id)
