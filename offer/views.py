from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from offer.models import Offer
from listing.models import Listing
from offer.forms.offer_form import OfferCreateForm, OfferUpdateForm
import datetime


def make_offer(request, listing_id):

    """
    This function takes as it's input a listing_id.
    It sends the user to a page where they can make an offer on that listing.
    It then creates the offer in the database and redirects the user to the listing.
    """

    if request.method == 'POST':
        form = OfferCreateForm(data=request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.listing = get_object_or_404(Listing, pk=listing_id)
            offer.buyer = get_object_or_404(User, pk=request.user.id)
            offer.placed = datetime.datetime.now()
            offer.accepted = False
            offer.save()
            return redirect('listing-details', id=listing_id)
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

# TODO: get_offers_by_buyer is not used atm, is it needed?
def get_offers_by_buyer(request, buyer_id):

    """
    This function takes as it's input a user_id.
    It returns a page with a list of offers made by the user.
    """
    offers = Offer.objects.all().filter(buyer_id=buyer_id).order_by('-amount')
    paginator = Paginator(offers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'offer/offer_list.html', {'page_obj': page_obj})


def cancel_offer(request, offer_id):

    """
    This function takes as it's input an offer_id. The offer in question is deleted from the database.
    """

    # TODO: Hvað ef offer er accepted, á að vera hægt að cancela því?
    offer = get_object_or_404(Offer, pk=offer_id)
    listing_id = offer.listing.id
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
        # TODO: Send user a notification
        # TODO: Success message: "You have accepted the offer"
        return redirect('listing-details', id=listing.id)
    else:
        # TODO: Error message: "Offer is already accepted"
        return redirect('listing-details', id=get_object_or_404(Listing, pk=offer.listing_id).id)


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
