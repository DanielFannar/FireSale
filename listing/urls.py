from django.urls import path
import offer.views
from . import views

urlpatterns = [
    # http://localhost:8000/listing
    path('', views.get_all_listings, name="listings"),
    path('<int:listing_id>/details', views.get_listing_by_id, name="listing-details"),
    path('add', views.add_listing, name="add-listing"),
    path('<int:listing_id>/remove', views.remove_listing, name="remove-listing"),
    path('<int:listing_id>/update', views.update_listing, name="update-listing"),
    path('<int:listing_id>/make_offer', offer.views.make_offer, name="make-offer")
]
