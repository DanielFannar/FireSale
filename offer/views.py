from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
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
            offer.placed = datetime.datetime.now()
            offer.accepted = False
            offer.save()
            notification_message = 'You have received an offer for your listing: ' + offer.listing.name
            send_notification(offer.listing.seller.id, notification_message)
            return redirect('listing-details', listing_id=listing_id)
    else:
        form = OfferCreateForm()
    return render(request, 'offer/make_offer.html', {
        'form': form,
        'listing': get_object_or_404(Listing, pk=listing_id)
    })

# TODO: get_offers_by_listing is not used atm, is it needed?
def get_offers_by_listing(request, listing_id):

    """
    This function takes as it's input a listing_id.
    It returns a page with a list of offers made on that listing.
    """
    offers = Offer.objects.all().filter(listing_id=listing_id).order_by('-amount')
    paginator = Paginator(offers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'offer/offer_list.html', {'page_obj': page_obj})


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

    # TODO: Hvað ef offer er accepted, á að vera hægt að cancela því?
    offer = get_object_or_404(Offer, pk=offer_id)
    listing_id = offer.listing.id
    if offer.accepted:
        notification_message = offer.buyer.username + ' has cancelled the offer you accepted on ' + offer.listing.name
        send_notification(offer.listing.seller, notification_message)
    offer.delete()
    return redirect('listing-details', id=listing_id)


def accept_offer(request, offer_id):

    """
    This function takes as it's input an offer_id.
    The offer in question is marked as accepted. The listing the offer was made on is marked unavailable.
    """

    offer = get_object_or_404(Offer, pk=offer_id)
    if offer.accepted is False:
        listing = get_object_or_404(Listing, pk=offer.listing_id)
        offer.accepted = True
        listing.available = False
        notification_message = \
            'Congratulations! Your offer on ' + listing.name + ' has been accepted, please go to http://127.0.0.1:8000/checkout_contact_info/' + str(offer_id) + '/checkout to complete your purchase.'
        send_notification(offer.buyer.id, notification_message)
        messages.success(request, 'Offer accepted!')
        return redirect('listing-details', listing_id=listing.id)
    else:
        # TODO: Error message: "Offer is already accepted"
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
            offer.save() # TODO: Give success and error messages
        return redirect('listing-details', id=offer.listing.id)
    else:
        form = OfferUpdateForm(instance=instance)
        return render(request, 'offer/update_offer.html', {
            'form': form,
            'offer_id': offer_id
        })