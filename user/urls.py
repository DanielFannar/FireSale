from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
import listing.views as lviews #ER ÞETTA KOSHER???
from . import views

urlpatterns = [
    # http://localhost:8000/candies
    path('', views.index, name="index"),
    path('<int:user_id>/listings', lviews.get_user_listings, name="user-listings"), #VILJUM VIÐ ÞETTA??
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile', views.profile, name='profile')
]