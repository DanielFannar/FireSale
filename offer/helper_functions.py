from django.shortcuts import get_object_or_404

from offer.models import Offer
from user.helper_functions import send_notification


def decline_offer(offer_id):
    offer = get_object_or_404(Offer, pk=offer_id)
    notification_message = 'Your offer on ' + offer.listing.name + ' has been declined'
    send_notification(offer.buyer.id, notification_message)
    offer.delete()