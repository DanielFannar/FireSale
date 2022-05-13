from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import timezone

from listing.helper_functions import listing_has_accepted_offer
from offer.models import Offer
from listing.models import Listing
from offer.forms.offer_form import OfferCreateForm, OfferUpdateForm
import datetime
from user.helper_functions import send_notification


def make_offer(request, listing_id):

    """
    This function takes as it's input a listing_id.
    It sends the user to a page where they can make an offer on that listing.
    It then creates the offer in the database and redirects the user to the listing.
    """
    # TODO: Make_offer should update a user's offer if they have already made an offer on the listing
    if request.method == 'POST':
        form = OfferCreateForm(data=request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.listing = get_object_or_404(Listing, pk=listing_id)
            offer.buyer = get_object_or_404(User, pk=request.user.id)
            offer.placed = timezone.now()
            offer.accepted = False
            offer.save()
            notification_message = 'You have received an offer for your listing: ' + offer.listing.name
            notification_url = redirect('listing-details', listing_id=listing_id)['Location']
            send_notification(offer.listing.seller.id, notification_message, notification_url)
            messages.success(request, 'Offer made!')
            return redirect('listing-details', listing_id=listing_id)
        else:
            messages.error(request, 'Error in submitting the offer.')
    else:
        form = OfferCreateForm()
    return render(request, 'offer/make_offer.html', {
        'form': form,
        'listing': get_object_or_404(Listing, pk=listing_id)
    })

# # TODO: get_offers_by_listing is not used atm, is it needed?
# def get_offers_by_listing(request, listing_id):
#
#     """
#     This function takes as it's input a listing_id.
#     It returns a page with a list of offers made on that listing.
#     """
#     offers = Offer.objects.all().filter(listing_id=listing_id).order_by('-amount')
#     paginator = Paginator(offers, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'offer/offer_list.html', {'page_obj': page_obj})


def get_offers_by_buyer(request, buyer_id):

    """
    This function takes as it's input a user_id.
    It returns a page with a list of offers made by the user.
    """
    offers = Offer.objects.all().filter(buyer_id=buyer_id)
    paginator = Paginator(offers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'offer/user_offers.html', {
        'page_obj': page_obj,
        'buyer': get_object_or_404(User, pk=buyer_id)})


def cancel_offer(request, offer_id):

    """
    This function takes as it's input an offer_id. The offer in question is deleted from the database.
    """

    offer = get_object_or_404(Offer, pk=offer_id)
    listing_id = offer.listing.id
    if offer.accepted:
        notification_message = offer.buyer.username + ' has cancelled the offer you accepted on ' + offer.listing.name
        notification_url = redirect('listing-details', listing_id=listing_id)['Location']
        send_notification(offer.listing.seller, notification_message, notification_url)
        offer.listing.available = True
    offer.delete()
    messages.success(request, 'Offer cancelled!')
    return redirect('listing-details', listing_id=listing_id)


def accept_offer(request, offer_id):

    """
    This function takes as it's input an offer_id.
    The offer in question is marked as accepted. The listing the offer was made on is marked unavailable.
    """

    offer = get_object_or_404(Offer, pk=offer_id)
    if listing_has_accepted_offer(offer.listing) == False:
        listing = get_object_or_404(Listing, pk=offer.listing_id)
        offer.accepted = True
        listing.available = False
        offer.save()
        listing.save()
        notification_message = \
            'Congratulations! Your offer on ' + listing.name + ' has been accepted!'
        notification_url = redirect('checkout-contact-info', offer_id=offer.id)['Location']
        send_notification(offer.buyer.id, notification_message, notification_url)
        messages.success(request, 'Offer accepted!')
        return redirect('listing-details', listing_id=listing.id)
    else:
        messages.error(request, 'This listing already has an accepted offer.')
        return redirect('listing-details', listing_id=offer.listing_id)


def update_offer(request, offer_id):

    """
    This function takes as it's input an offer_id.
    If the offer has not been accepted, it sends the user to a page where they can input a new amount for the offer.
    It then updates the amount on the offer and redirects the user to the listing.
    """

    instance = get_object_or_404(Offer, pk=offer_id)
    if request.method == 'POST':
        form = OfferUpdateForm(data=request.POST, instance=instance)

        if form.is_valid() and instance.accepted is False:
            offer = form.save(commit=False)
            offer.listing = get_object_or_404(Listing, pk=instance.listing.id)
            offer.buyer = get_object_or_404(User, pk=request.user.id)
            offer.placed = datetime.datetime.now()
            offer.accepted = False
            offer.save()
            messages.success(request, 'Your offer has been updated!')
        else:
            messages.error(request, 'Your offer could not be updated.')
        return redirect('listing-details', listing_id=offer.listing.id)
    else:
        form = OfferUpdateForm(instance=instance)
        return render(request, 'offer/update_offer.html', {
            'form': form,
            'offer_id': offer_id
        })
