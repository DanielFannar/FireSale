from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import request
from django.shortcuts import get_object_or_404
from django.utils import timezone

from offer.models import Offer
from user.models import Message, UserProfile, Notification

def send_notification(user_id, notification_message):
    user = get_object_or_404(User, pk=user_id)
    # user_profile = get_object_or_404(UserProfile, user=user)
    notification = Notification(recipient=user, content=notification_message, seen=False, sent=timezone.now())
    notification.save()
    # if user_profile.settings.email_notification == True:
    #     send_notification_mail(message.id)


def unread_notification_count():
    return 1

def user_has_unread_message():
    return Message.objects.all().filter(recipient_id=request.user.id, seen=False).count()
