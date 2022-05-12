from math import floor

from django import template
from django.db.models import Avg

from user.models import Message, Notification, Rating

register = template.Library()


@register.simple_tag
def number_of_unread_messages(request):
    number_of_unread_messages = Message.objects.all().filter(recipient_id=request.user.id, seen=False).count()
    if number_of_unread_messages == 0:
        number_of_unread_messages = ''
    return number_of_unread_messages

@register.simple_tag
def number_of_unread_notifications(request):
    number_of_unread_notifications = Notification.objects.all().filter(recipient_id=request.user.id, seen=False).count()
    if number_of_unread_notifications == 0:
        number_of_unread_notifications = ''
    return number_of_unread_notifications

@register.simple_tag
def user_star_rating(user_id):
    rating = Rating.objects.all().filter(ratee_id=user_id).aggregate(Avg('rating'))
    rating_number = rating['rating__avg']
    star_rating = ''
    if rating_number is None:
        star_rating= 'N/A'
    else:
        for i in range(floor(rating_number)):
            star_rating += '⭐'
        star_rating += ' (' + str(rating_number) + ')'
    return star_rating

