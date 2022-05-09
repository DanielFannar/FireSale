from django.db.models import Avg
from user.models import Rating


def get_user_rating(user_id):
    rating = Rating.objects.all().filter(ratee_id=user_id).aggregate(Avg('rating'))
    if rating['rating__avg'] is None:
        rating['rating__avg'] = 'N/A'
    return rating['rating__avg']
