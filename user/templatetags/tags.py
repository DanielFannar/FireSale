from django import template

from user.models import Message, Notification

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