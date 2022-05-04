from django.urls import path
import listing.views as lviews #ER ÞETTA KOSHER???
from . import views

urlpatterns = [
    # http://localhost:8000/candies
    path('', views.index, name="edit_profile-index"),
    path('<int:user_id>/listings', lviews.get_user_listings, name="user-listings") #VILJUM VIÐ ÞETTA??
]