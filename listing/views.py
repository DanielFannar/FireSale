from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from listing.models import Listing, ListingImage
from listing.forms.listing_form import ListingCreateForm
import datetime

# Create your views here.


def get_listing_by_id(request, id):
    return render(request, 'listing/listingdetails.html', {
        'listing': get_object_or_404(Listing, pk=id)
    })


def get_all_listings(request):
    return render(request, 'listing/listings.html', {
        'listings': Listing.objects.all()
    })


def get_user_listings(request, user_id):
    return render(request, 'listing/listings.html', {
        'listings': Listing.objects.all().filter(seller_id=user_id)
    })


def add_listing(request):
    if request.method == 'POST':
        form = ListingCreateForm(data=request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = get_object_or_404(User, pk=1)
            listing.listed = datetime.datetime.now()
            listing.available = True
            listing.save()
            listing_image = ListingImage(image=request.POST['image'], listing=listing)
            listing_image.save()
    else:
        form = ListingCreateForm()
    return render(request, 'listing/add_listing.html', {
        'form': form
    })
