from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from offer.models import Offer
from listing.models import Listing
from offer.forms.offer_form import OfferCreateForm
import datetime

# Create your views here.


def get_offer_by_id(request, id):
    return render(request, 'listing/single_offer.html', {
        'offer': get_object_or_404(Offer, pk=id)
    })


def make_offer(request, listing_id):
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


def get_all_listing_offers(request, listing_id):
    return render(request, 'offer/offer_list.html', {
        'offers': Offer.objects.all().filter(listing_id=listing_id)
    })

'''



def get_user_listings(request, user_id):
    return render(request, 'listing/listings.html', {
        'listings': Listing.objects.all().filter(seller_id=user_id)
    })


def add_listing(request):
    if request.method == 'POST':
        form = ListingCreateForm(data=request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = get_object_or_404(User, pk=request.user.id)
            listing.listed = datetime.datetime.now()
            listing.available = True
            listing.save()
            listing_image = ListingImage(image=request.POST['image'], listing=listing)
            listing_image.save()
            return redirect('listing-details', id=listing.id)
    else:
        form = ListingCreateForm()
    return render(request, 'listing/add_listing.html', {
        'form': form
    })


def remove_listing(request, id):
    listing = get_object_or_404(Listing, pk=id)
    listing.delete()
    return redirect('listings')


def update_listing(request, id):
    instance = get_object_or_404(Listing, pk=id)
    if request.method == 'POST':
        form = ListingUpdateForm(data=request.POST, instance=instance)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = get_object_or_404(User, pk=request.user.id)
            listing.listed = datetime.datetime.now()
            listing.available = True
            listing.save()
            return redirect('listing-details', id=id)
    else:
        form = ListingUpdateForm(instance=instance)
        return render(request, 'listing/update_listing.html', {
            'form': form,
            'id': id
        })
'''