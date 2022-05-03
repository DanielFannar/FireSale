from django.shortcuts import render, get_object_or_404
from listing.models import Listing
# Create your views here.


def get_listing_by_id(request, id):
    return render(request, 'listing/listingdetails.html', {
        'listing': get_object_or_404(Listing, pk=id)
    })


def get_all_listings(request):
    return render(request, 'listing/listings.html', {
    'listings': Listing.objects.all()
    })


