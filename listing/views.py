from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Max
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from offer.models import Offer
from listing.models import Listing, ListingImage
from listing.forms.listing_form import ListingCreateForm, ListingUpdateForm
import datetime
from listing.helper_functions import *

# Create your views here.



def get_listing_by_id(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    offers = Offer.objects.all().filter(listing_id=listing_id).order_by('-amount')
    paginator = Paginator(offers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    list_of_listings = Listing.objects.all().filter(available=True).exclude(pk=listing_id)
    #mrp = most_related_products(listing, list_of_listings)
    #mrp = Listing.objects.filter(id__in=mrp)
    mrp = listing_relatedness_v2(listing)
    return render(request, 'listing/listingdetails.html', {
        'listing': listing,
        'mrp': mrp,
        'page_obj': page_obj
    })

def get_all_listings(request):
    listings = Listing.objects.all()

    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        listings = listings.filter(Q(name__icontains=search_filter)|Q(description__icontains=search_filter))
    if 'sort' in request.GET:
        sort = request.GET['sort']
        if sort == 'name':
            listings = listings.order_by('name')
        elif sort == 'price':
            max_offer_by_listing = Offer.objects.all().values('listing_id').annotate(Max('amount')).order_by('amount__max')
            listing_ids = []
            for listing in max_offer_by_listing:
                listing_ids.append(listing['listing_id'])
            listings = Listing.objects.filter(id__in=listing_ids)
            listings = dict([(listing.id, listing) for listing in listings])
            listings = [listings[id] for id in listing_ids]
        elif sort == 'datetime':
            listings = listings.order_by('-listed')

    paginator = Paginator(listings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listing/listings.html', {
        'page_obj': page_obj})


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
            messages.success(request, 'Listing added!')
            return redirect('listing-details', listing_id=listing.id)
        else:
            messages.error(request, 'Listing could not be added')
            return redirect('add-listing')
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
            messages.success(request, 'Listing updated!')
            return redirect('listing-details', listing.id)
        else:
            messages.error(request, 'Listing could not be updated')
            return redirect('listing-details', listing_id)
    else:
        form = ListingUpdateForm(instance=instance)
        return render(request, 'listing/update_listing.html', {
            'form': form,
            'listing_id': listing_id
        })






# TODO: Is this used anywhere?
# def related_products(request, listing_id):
#     listing = get_object_or_404(Listing, pk=listing_id)
#     list_of_listings = Listing.objects.all().filter(available=True)
#     mrp = most_related_products(listing, list_of_listings)
#     listings = Listing.objects.filter(id__in=mrp)
#     return render(request, 'listing/update_listing.html', {
#             'listings': listings,
#         })

