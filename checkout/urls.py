from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/checkout
    path('<int:purchase_id>/rate', views.rate_purchase, name="rate-purchase"),
    path('<int:offer_id>/checkout', views.checkout, name="checkout"),
    path('<int:purchase_id>/details', views.get_purchase_by_id, name="purchase-details")
]
