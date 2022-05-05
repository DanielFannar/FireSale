from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/checkout
    path('<int:purchase_id>/rate', views.rate_purchase, name="rate-purchase")
]
