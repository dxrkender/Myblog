"""URL configuration for the `accounts` app."""

from django.urls import path

from app.accounts.views import ProfileView

urlpatterns = [
    # path('login/'),
    # path('logout/'),
    # path('register/'),
    path('profile/<slug:slug>/', ProfileView.as_view(), name='profile'),
    # path('reset/'),
    # path('reset/done/'),
    # path('reset/confirm/<uidb64>/<token>/'),
]