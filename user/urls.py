from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/candies
    path('', views.index, name="index"),
    path('/editprofile', views.edit, name="edit")
]