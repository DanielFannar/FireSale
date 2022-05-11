from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from user.models import Rating, Message, UserProfile, Notification


def get_user_rating(user_id):
    rating = Rating.objects.all().filter(ratee_id=user_id).aggregate(Avg('rating'))
    if rating['rating__avg'] is None:
        rating['rating__avg'] = 'N/A'
    return rating['rating__avg']


def send_notification(user_id, notification_message):
    firesale = get_object_or_404(User, pk=1337)
    user = get_object_or_404(User, pk=user_id)
    # user_profile = get_object_or_404(UserProfile, user=user)
    message = Message(recipient=user, content=notification_message, sender=firesale)
    message.save()
    # if user_profile.settings.email_notification == True:
    #     send_notification_mail(message.id)


def user_has_unread_notification(user_id):
    if Notification.objects.all().filter(recipient_id=user_id, seen=False).count == 0:
        return False
    else:
        return True


def user_has_unread_message(user_id):
    if Message.objects.all().filter(recipient_id=user_id, seen=False).count == 0:
        return False
    else:
        return True
