from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from checkout.forms.contact_info_form import ContactInfoCreateForm
from checkout.forms.payment_info_form import PaymentInfoCreateForm
from checkout.models import Purchase
from user.forms.rating_form import RatingCreateForm



# TODO: Hugsa það hvernig checkout process virkar, ekki viss um að við viljum hafa rate_purchase view.

def rate_purchase(request, purchase_id):
    user = request.user
    purchase = get_object_or_404(Purchase, pk=purchase_id)

    if request.method == 'POST':
        form = RatingCreateForm(data=request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.rater = user
            rating.ratee = purchase.offer.listing.seller
            rating.save()
            return redirect('user-ratings', user_id=rating.ratee.id)
    else:
        form = RatingCreateForm()
    return render(request, 'checkout/rate_purchase.html', {
        'form': form,
        'purchase_id': purchase_id
    })


def checkout(request, offer_id):
    user = request.user

    if request.method == 'POST':

        contact_info_form = ContactInfoCreateForm(request.POST)
        payment_info_form = PaymentInfoCreateForm(request.POST)
        if contact_info_form.is_valid() and payment_info_form.is_valid():
            contact_info = contact_info_form.save(commit=False)
            payment_info = payment_info_form.save(commit=False)
            contact_info.user = user
            payment_info.user = user
            contact_info_form.save()
            payment_info_form.save()
            purchase = Purchase(offer_id=offer_id, contact_info=contact_info, payment_info=payment_info)
            purchase.save()
            return redirect('purchase-details', purchase_id=purchase.id)
    else:
        contact_info_form = ContactInfoCreateForm()
        payment_info_form = PaymentInfoCreateForm()
        return render(request, 'checkout/checkout.html', {
            'contact_info_form': contact_info_form,
            'payment_info_form': payment_info_form
    })


def get_purchase_by_id(request, purchase_id):
    return render(request, 'checkout/purchase_details.html', {
        'purchase': get_object_or_404(Purchase, pk=purchase_id),
    })


def get_user_purchases(request, user_id):
    purchases = Purchase.objects.all().filter(offer__buyer_id=user_id)
    paginator = Paginator(purchases, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'checkout/purchases.html', {'page_obj': page_obj})