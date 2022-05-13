from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/checkout
    path('<int:purchase_id>/rate', views.rate_purchase, name="rate-purchase"),
    path('<int:purchase_id>/details', views.get_purchase_by_id, name="purchase-details"),
    path('<int:offer_id>/checkout_contact_info', views.checkout_contact_info, name="checkout-contact-info"),
    path('<int:offer_id>/checkout_payment_info', views.checkout_payment_info, name="checkout-payment-info"),
    path('<int:offer_id>/checkout_confirm', views.checkout_confirm, name="checkout-confirm"),
    path('<int:user_id>/purchases', views.get_user_purchases, name="purchases")
]
