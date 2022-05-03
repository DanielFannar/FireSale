from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/listing
    path('', views.get_all_listings, name="listings"),
    path('<int:id>/details', views.get_listing_by_id, name="listing-details")
]