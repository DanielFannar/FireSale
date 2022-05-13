from django.shortcuts import render
from user.models import User
from offer.models import Offer
from listing.models import Listing

# Create your views here.
def index(request):
    current_user = request.user
    return render(request, 'fire_sale/frontpage.html', {
        'current_user': current_user})


def statistics(request):
    total_users = len(User.objects.all())
    total_offers =  len(Offer.objects.all())
    total_listings =  len(Listing.objects.all())
    if request.user.is_authenticated:
        curr_user_listings = Listing.objects.all().filter(seller=request.user).count()
        curr_user_offers = Offer.objects.all().filter(buyer_id=request.user).count()
        return render(request, '../templates/Misc/statistics.html', {
            'total_users': total_users,
            'total_offers': total_offers,
            'total_listings': total_listings,
            'curr_user_listings': curr_user_listings,
            'curr_user_offers': curr_user_offers})
    else:
        return render(request, '../templates/Misc/statistics.html', {
            'total_users': total_users,
            'total_offers': total_offers,
            'total_listings': total_listings})

