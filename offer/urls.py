from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/candies
    path('<id:int>/details', views.get_offer_by_id, name="offer-details")

]