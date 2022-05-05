from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from offer.models import Offer
from listing.models import Listing, ListingImage
from listing.forms.listing_form import ListingCreateForm, ListingUpdateForm
import datetime

# Create your views here.


def get_listing_by_id(request, id):
    offers = Offer.objects.all().filter(listing_id=id).order_by('-amount')
    paginator = Paginator(offers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listing/listingdetails.html', {
        'listing': get_object_or_404(Listing, pk=id),
        'page_obj': page_obj
    })


def get_all_listings(request):
    listings = Listing.objects.all()
    paginator = Paginator(listings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listing/listings.html', {'page_obj': page_obj})


def get_user_listings(request, user_id):

    listings = Listing.objects.all().filter(seller_id=user_id)
    paginator = Paginator(listings, 10)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listing/listings.html', {'page_obj': page_obj})


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
