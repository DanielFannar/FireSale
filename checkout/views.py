from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse
# Create your views here.
from checkout.models import Purchase
from user.forms.profile_form import CreateRatingForm


# TODO: Hugsa það hvernig checkout process virkar, ekki viss um að við viljum hafa rate_purchase view.
def rate_purchase(request, purchase_id):
    user = request.user
    purchase = get_object_or_404(Purchase, pk=purchase_id)

    if request.method == 'POST':
        form = CreateRatingForm(data=request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.rater = user
            rating.ratee = purchase.offer.listing.seller
            rating.save()
            return redirect('user-ratings', user_id=rating.ratee.id)
    else:
        form = CreateRatingForm()
    return render(request, 'checkout/rate_purchase.html', {
        'form': form,
        'purchase_id': purchase_id
    })