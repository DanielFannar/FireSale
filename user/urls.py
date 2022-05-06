from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
import listing.views
import offer.views
from . import views

urlpatterns = [
    # http://localhost:8000/user

    path('<int:user_id>/listings', listing.views.get_user_listings, name='user-listings'),
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('<int:user_id>/profile', views.get_profile, name='user-profile'),
    path('profile', views.get_profile, name='my-profile'),
    path('edit_profile', views.edit_profile, name='edit-profile'),
    path('<int:buyer_id>/offers_made', offer.views.get_offers_by_buyer, name='offers-made'),
    path('<int:user_id>/ratings', views.get_user_ratings, name='user-ratings'),
    path('<int:to_user_id>/send_message', views.send_message, name='send-message'),
    path('send_message', views.send_message, name='send-message'),
    path('<int:user_id>/messages', views.get_message_chain, name='message-chain'),
    # TODO: Is this needed? path('messages',views.get_user_message_chains, name='messages'),
    path('<int:message_id>/message', views.get_message_by_id, name='single-message')
]