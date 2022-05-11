from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/candies
    path('', views.index, name="/"),
    path('statistics', views.statistics, name="statistics")
]