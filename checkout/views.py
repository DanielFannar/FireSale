from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from checkout.forms.contact_info_form import ContactInfoCreateForm
from checkout.forms.payment_info_form import PaymentInfoCreateForm
from checkout.models import Purchase, PaymentInfo, ContactInfo, Country
from listing.models import Listing
from offer.helper_functions import decline_offer
from offer.models import Offer
from user.forms.rating_form import RatingCreateForm
from user.helper_functions import send_notification


def rate_purchase(request, purchase_id):
    """This view let's a user create a rating for a specific purchase.
    Only one rating can be given for each purchase."""

    user = request.user
    purchase = get_object_or_404(Purchase, pk=purchase_id)

    if request.method == 'POST':
        form = RatingCreateForm(data=request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.rater = user
            rating.ratee = purchase.offer.listing.seller
            rating.purchase = purchase
            rating.save()
            notification_message = purchase.offer.buyer.username + ' has given you a rating for ' + purchase.offer.listing.name + '.'
            notification_url = redirect('user-ratings', user_id=rating.ratee.id)['Location']
            send_notification(purchase.offer.listing.seller.id, notification_message, notification_url)
            messages.success(request, 'Rating submitted!')
            return redirect('user-ratings', user_id=rating.ratee.id)
        else:
            messages.error(request, 'There was an error with submitting the rating.')
            return redirect('rate-purchase', purchase_id=purchase_id)
    else:
        form = RatingCreateForm()
    return render(request, 'checkout/rate_purchase.html', {
        'form': form,
        'purchase': purchase
    })


def checkout_contact_info(request, offer_id):
    """This view takes the user to the first step in the checkout procedure.
    The offer with the given offer_id determines the price and product being checked out.
    If the offer hasn't been accepted or the listing has already been purchased, checkout is not possible."""
    fields = ['full_name', 'country', 'city', 'street_name', 'house_number', 'postal_code']
    offer = get_object_or_404(Offer, pk=offer_id)
    if offer.accepted and not offer.listing.purchased:
        if request.method == 'POST':
            contact_info_form = ContactInfoCreateForm(request.POST)
            if contact_info_form.is_valid():
                for field in fields:
                    request.session[field] = contact_info_form.cleaned_data[field]
                request.session['country'] = request.session['country'].id
                request.session['full_name'] = contact_info_form.cleaned_data['full_name']
                return redirect('checkout-payment-info', offer_id=offer_id)

        else:
            initial = {}
            for field in fields:
                initial[field] = request.session.get(field)
            contact_info_form = ContactInfoCreateForm(initial=initial)
            return render(request, 'checkout/checkout_contact_info.html', {
                'offer_id': offer_id,
                'contact_info_form': contact_info_form
            })
    else:
        messages.error(request, 'This is not a valid offer for checkout.')
        return redirect('listing-details', listing_id = offer.listing.id)


def checkout_payment_info(request, offer_id):
    """This view is the second step of the checkout process.
    The fields from the previous step are saved in the session so the user can
    easily move back and forth between steps."""
    fields = ['name', 'card_number', 'expiration_date', 'cvc']
    if request.method == 'POST':
        payment_info_form = PaymentInfoCreateForm(request.POST)
        if payment_info_form.is_valid():

            for field in fields:
                request.session[field] = payment_info_form.cleaned_data[field]
            return redirect('checkout-confirm', offer_id=offer_id)
        else:
            messages.error(request, 'Invalid payment information')
            return redirect('checkout-payment-info', offer_id=offer_id)

    else:
        initial = {}
        for field in fields:
            initial[field] = request.session.get(field)
        payment_info_form = PaymentInfoCreateForm(initial=initial)
        return render(request, 'checkout/checkout_payment_info.html', {
            'offer_id': offer_id,
            'payment_info_form': payment_info_form
        })


def checkout_confirm(request, offer_id):
    """The last step in the checkout process.
    Presents the user with the information they have given. And asks them to confirm.
    If the user confirms the purchase is finalized.
    All other offers on that listing are then declined."""
    offer = get_object_or_404(Offer, pk=offer_id)
    listing = get_object_or_404(Listing, pk=offer.listing.id)
    contact_info_fields = ['full_name', 'country', 'city', 'street_name', 'house_number', 'postal_code']
    payment_info_fields = ['name', 'card_number', 'expiration_date', 'cvc']
    if request.method == 'POST':
        payment_info = PaymentInfo(user=request.user,
                                   name=request.session.get('name'),
                                   card_number=request.session.get('card_number'),
                                   expiration_date=request.session.get('expiration_date'),
                                   cvc=request.session.get('cvc'))
        contact_info = ContactInfo(user=request.user,
                                   full_name=request.session.get('full_name'),
                                   country=get_object_or_404(Country, pk=request.session.get('country')),
                                   city=request.session.get('city'),
                                   street_name=request.session.get('street_name'),
                                   house_number=request.session.get('house_number'),
                                   postal_code=request.session.get('postal_code'))
        payment_info.save()
        contact_info.save()
        purchase = Purchase(payment_info=payment_info, contact_info=contact_info, offer=offer)
        purchase.save()
        notification_message = 'Purchase for ' + purchase.offer.listing.name + ' has been completed! The money will magically appear in your back pocket in 3-5 business days.'
        notification_url = redirect('purchase-details', purchase_id=purchase.id)['Location']
        send_notification(listing.seller.id, notification_message, notification_url)
        listing.purchased = True
        listing.available = False
        listing.save()
        offers = Offer.objects.all().filter(listing=listing).exclude(pk=offer.id)
        for o in offers:
            decline_offer(o.id)  # Declining all other offers.
        for field in contact_info_fields:
            request.session[field] = ''  # Clearing the session.
        for field in payment_info_fields:
            request.session[field] = ''  # Clearing the session.
        messages.success(request, 'Purchase completed!')
        return redirect('purchase-details', purchase_id=purchase.id)
    else:

        contact_info_initial = {}
        payment_info_initial = {}
        for field in contact_info_fields:
            contact_info_initial[field] = request.session.get(field)
        for field in payment_info_fields:
            payment_info_initial[field] = request.session.get(field)
        contact_info_form = ContactInfoCreateForm(initial=contact_info_initial)
        payment_info_form = PaymentInfoCreateForm(initial=payment_info_initial)
        return render(request, 'checkout/checkout_confirm.html', {
            'contact_info_form': contact_info_form,
            'payment_info_form': payment_info_form,
            'listing': listing,
            'offer_id': offer_id
        })


# This is the old checkout procedure.
# def checkout(request, offer_id):
#     user = request.user
#
#     if request.method == 'POST':
#
#         contact_info_form = ContactInfoCreateForm(request.POST)
#         payment_info_form = PaymentInfoCreateForm(request.POST)
#         if contact_info_form.is_valid() and payment_info_form.is_valid():
#
#             contact_info = contact_info_form.save(commit=False)
#             payment_info = payment_info_form.save(commit=False)
#             contact_info.user = user
#             payment_info.user = user
#             contact_info_form.save()
#             payment_info_form.save()
#             purchase = Purchase(offer_id=offer_id, contact_info=contact_info, payment_info=payment_info)
#             purchase.save()
#             return redirect('purchase-details', purchase_id=purchase.id)
#     else:
#         contact_info_form = ContactInfoCreateForm()
#         payment_info_form = PaymentInfoCreateForm()
#         return render(request, 'checkout/checkout.html', {
#             'contact_info_form': contact_info_form,
#             'payment_info_form': payment_info_form
#     })


def get_purchase_by_id(request, purchase_id):
    """This view presents the user with a single purchase with the given purchase_id."""
    return render(request, 'checkout/purchase_details.html', {
        'purchase': get_object_or_404(Purchase, pk=purchase_id),
    })


def get_user_purchases(request, user_id):
    """This view presents the user with all purchases completed by a user with the given user_id.
    This can be another user or the same user."""
    purchases = Purchase.objects.all().filter(offer__buyer_id=user_id)
    paginator = Paginator(purchases, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'checkout/purchases.html', {
        'page_obj': page_obj,
        'buyer': get_object_or_404(User, pk=user_id)})
