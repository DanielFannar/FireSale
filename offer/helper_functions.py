from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from offer.models import Offer
from user.helper_functions import send_notification



def decline_offer(offer_id):
    """This function declines the offer with the given offer_id.
    It sends a notification to the user that made the offer."""
    offer = get_object_or_404(Offer, pk=offer_id)
    listing = offer.listing
    notification_message = 'Your offer on ' + offer.listing.name + ' has been declined'
    notification_url = redirect('listing-details', listing_id=offer.listing.id)['Location']
    send_notification(offer.buyer.id, notification_message, notification_url)
    send_notification(offer.buyer.id, notification_message, notification_url)
    offer.delete()