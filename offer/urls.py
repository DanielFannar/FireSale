from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/offer
    path('<int:offer_id>/accept', views.accept_offer, name="accept-offer"),
    path('<int:offer_id>/cancel', views.cancel_offer, name="cancel-offer"),
    path('<int:offer_id>/update', views.update_offer, name="update-offer")
]