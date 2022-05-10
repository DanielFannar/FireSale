from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from offer.models import Offer
from listing.models import Listing, ListingImage
from listing.forms.listing_form import ListingCreateForm, ListingUpdateForm
import datetime

# Create your views here.


def get_listing_by_id(request, listing_id):
    user = get_object_or_404(User, pk=request.user.id)
    offers = Offer.objects.all().filter(listing_id=listing_id).order_by('-amount')
    paginator = Paginator(offers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listing/listingdetails.html', {
        'listing': get_object_or_404(Listing, pk=listing_id),
        'page_obj': page_obj,
        'user': user
    })


def get_all_listings(request):
    listings = Listing.objects.all()
    listings_and_highest_offer = []
    for listing in listings:
        offer = Offer.objects.all().filter(listing_id=listing.id).order_by('-amount').first()
        if offer is None:
            offer = {'amount': 'No offers yet!'}
        listings_and_highest_offer.append([listing, offer])
    paginator = Paginator(listings_and_highest_offer, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listing/listings.html', {'page_obj': page_obj})


def get_user_listings(request, user_id):
    listings = Listing.objects.all().filter(seller_id=user_id)
    listings_and_highest_offer = []
    for listing in listings:
        offer = Offer.objects.all().filter(listing_id=listing.id).order_by('-amount').first()
        listings_and_highest_offer.append([listing,offer])
    paginator = Paginator(listings_and_highest_offer, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listing/user_listings.html', {
        'page_obj': page_obj,
        'seller': get_object_or_404(User, pk=user_id)})


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
            return redirect('listing-details', listing_id=listing.id)
    else:
        form = ListingCreateForm()
    return render(request, 'listing/add_listing.html', {
        'form': form
    })


def remove_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    listing.delete()
    return redirect('listings')


def update_listing(request, listing_id):
    instance = get_object_or_404(Listing, pk=listing_id)
    if request.method == 'POST':
        form = ListingUpdateForm(data=request.POST, instance=instance)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = get_object_or_404(User, pk=request.user.id)
            listing.listed = datetime.datetime.now()
            listing.available = True
            listing.save()
            return redirect('listing-details', listing.id)
    else:
        form = ListingUpdateForm(instance=instance)
        return render(request, 'listing/update_listing.html', {
            'form': form,
            'listing_id': listing_id
        })


def decline_all_other_offers(offer_id):
    offer = get_object_or_404(Offer, offer_id)
    listing = get_object_or_404(Listing, pk=offer.id)
    offers_to_decline = Offer.objects.all().filter('listing')