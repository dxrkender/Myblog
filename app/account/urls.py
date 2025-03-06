# -*- coding: UTF-8 -*-
"""URL configuration for the `account` application."""

from django.contrib.auth.decorators import login_required
from django.urls import path

from app.account.views import (
    AccountLoginView,
    AccountLogoutView,
    AccountPasswordResetCompleteView,
    AccountPasswordResetConfirmView,
    AccountPasswordResetDoneView,
    AccountPasswordResetView,
    AccountProfileDetailView,
    AccountProfileUpdateView,
    AccountSingUpView,
)

urlpatterns = [
    path("login/", AccountLoginView.as_view(), name="login"),
    path("logout/", AccountLogoutView.as_view(), name="logout"),
    path("signup/", AccountSingUpView.as_view(), name="signup"),
    path(
        "profile/<slug:slug>/",
        login_required(AccountProfileDetailView.as_view()),
        name="profile_detail",
    ),
    path(
        "profile/edit/<slug:slug>/",
        login_required(AccountProfileUpdateView.as_view()),
        name="profile_edit",
    ),
    path(
        "password-reset/",
        AccountPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done",
        AccountPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        AccountPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        AccountPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
