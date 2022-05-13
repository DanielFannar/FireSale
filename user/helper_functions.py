from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Avg
from django.http import request
from django.shortcuts import get_object_or_404
from django.utils import timezone

from offer.models import Offer
from user.models import Message, UserProfile, Notification


def send_notification(user_id, notification_message, url):
    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    notification = Notification(recipient=user,
                                content=notification_message,
                                seen=False, sent=timezone.now(),
                                url='http://127.0.0.1:8000'+url)
    notification.save()
    if user_profile.settings.email_notification == True:
        send_notification_mail(notification.id)


def send_notification_mail(notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    send_mail(
        'You have received a notification from FireSale',
        notification.content + '\n Please go to ' + notification.url + ' for more details.',
        'firesale.ehf@gmail.com',
        [notification.recipient.email],
        fail_silently=False,
    )