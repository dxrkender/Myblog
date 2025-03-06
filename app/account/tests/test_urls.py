import pytest
from django.urls import reverse, resolve
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


class TestAccountUrls:
    def test_login_url(self):
        """Test the login URL."""
        url = reverse("account:login")
        assert (
            url == "/account/login/"
        ), "Login URL should match the expected pattern"
        resolver = resolve("/account/login/")
        assert (
            resolver.func.view_class == AccountLoginView
        ), "Login URL should resolve to AccountLoginView"

    def test_logout_url(self):
        """Test the logout URL."""
        url = reverse("account:logout")
        assert (
            url == "/account/logout/"
        ), "Logout URL should match the expected pattern"
        resolver = resolve("/account/logout/")
        assert (
            resolver.func.view_class == AccountLogoutView
        ), "Logout URL should resolve to AccountLogoutView"

    def test_signup_url(self):
        """Test the signup URL."""
        url = reverse("account:signup")
        assert (
            url == "/account/signup/"
        ), "Signup URL should match the expected pattern"
        resolver = resolve("/account/signup/")
        assert (
            resolver.func.view_class == AccountSingUpView
        ), "Signup URL should resolve to AccountSingUpView"

    def test_profile_detail_url(self):
        """Test the profile detail URL."""
        slug = "test-slug"
        url = reverse("account:profile_detail", args=[slug])
        assert (
            url == f"/account/profile/{slug}/"
        ), "Profile detail URL should match the expected pattern"
        resolver = resolve(f"/account/profile/{slug}/")
        assert (
            resolver.func.view_class == AccountProfileDetailView
        ), "Profile detail URL should resolve to AccountProfileDetailView"
        assert (
            resolver.url_name == "profile_detail"
        ), "URL name should be 'profile_detail'"

    def test_profile_edit_url(self):
        """Test the profile edit URL."""
        slug = "test-slug"
        url = reverse("account:profile_edit", args=[slug])
        assert (
            url == f"/account/profile/edit/{slug}/"
        ), "Profile edit URL should match the expected pattern"
        resolver = resolve(f"/account/profile/edit/{slug}/")
        assert (
            resolver.func.view_class == AccountProfileUpdateView
        ), "Profile edit URL should resolve to AccountProfileUpdateView"
        assert (
            resolver.url_name == "profile_edit"
        ), "URL name should be 'profile_edit'"

    def test_password_reset_url(self):
        """Test the password reset URL."""
        url = reverse("account:password_reset")
        assert (
            url == "/account/password-reset/"
        ), "Password reset URL should match the expected pattern"
        resolver = resolve("/account/password-reset/")
        assert (
            resolver.func.view_class == AccountPasswordResetView
        ), "Password reset URL should resolve to AccountPasswordResetView"

    def test_password_reset_done_url(self):
        """Test the password reset done URL."""
        url = reverse("account:password_reset_done")
        assert (
            url == "/account/password-reset/done"
        ), "Password reset done URL should match the expected pattern"
        resolver = resolve("/account/password-reset/done")
        assert (
            resolver.func.view_class == AccountPasswordResetDoneView
        ), "Password reset done URL should resolve to AccountPasswordResetDoneView"

    def test_password_reset_confirm_url(self):
        """Test the password reset confirm URL."""
        uidb64 = "mock-uidb64"
        token = "mock-token"
        url = reverse("account:password_reset_confirm", args=[uidb64, token])
        assert (
            url == f"/account/password-reset/{uidb64}/{token}/"
        ), "Password reset confirm URL should match the expected pattern"
        resolver = resolve(f"/account/password-reset/{uidb64}/{token}/")
        assert (
            resolver.func.view_class == AccountPasswordResetConfirmView
        ), "Password reset confirm URL should resolve to AccountPasswordResetConfirmView"
        assert (
            resolver.url_name == "password_reset_confirm"
        ), "URL name should be 'password_reset_confirm'"

    def test_password_reset_complete_url(self):
        """Test the password reset complete URL."""
        url = reverse("account:password_reset_complete")
        assert (
            url == "/account/password-reset/complete/"
        ), "Password reset complete URL should match the expected pattern"
        resolver = resolve("/account/password-reset/complete/")
        assert (
            resolver.func.view_class == AccountPasswordResetCompleteView
        ), "Password reset complete URL should resolve to AccountPasswordResetCompleteView"
