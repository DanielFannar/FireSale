from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/listing
    path('', views.get_all_listings, name="listings"),
    path('<int:id>/details', views.get_listing_by_id, name="listing-details"),
    path('add', views.add_listing, name="add-listing"),
    path('<int:id>/remove', views.remove_listing, name="remove-listing"),
    path('<int:id>/update', views.update_listing, name="update-listing")
]
