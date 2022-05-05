from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
import listing.views
import offer.views
from . import views

urlpatterns = [
    # http://localhost:8000/user

    path('<int:user_id>/listings', listing.views.get_user_listings, name="user-listings"),
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('<int:user_id>/profile', views.profile, name='user-profile'),
    path('profile', views.profile, name='profile'), # Henda?
    path('<int:buyer_id>/offers_made', offer.views.get_offers_by_buyer, name='offers-made')
]