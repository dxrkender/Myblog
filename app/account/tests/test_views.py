# -*- coding: UTF-8 -*-
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from app.account.views import (
    AccountLoginView,
    AccountSingUpView,
    AccountProfileDetailView,
    AccountProfileUpdateView,
    AccountPasswordResetView,
)
from app.account.models import Account
from app.tests.conftest import factory, users


class TestAccountViews:
    # Тесты для AccountLoginView
    def test_login_view_get_unauthenticated(self, factory, mocker):
        request = factory.get(reverse("account:login"))
        request.user = mocker.Mock(is_authenticated=False)

        response = AccountLoginView.as_view()(request)

        assert response.status_code == 200
        assert "title" in response.context_data
        assert response.context_data["title"] == "Log in"

    def test_login_view_authenticated_redirect(self, factory, users):
        request = factory.get(reverse("account:login"))
        request.user = users["user"]

        response = AccountLoginView.as_view()(request)

        assert isinstance(response, HttpResponseRedirect)
        assert response.url == reverse("core:index")

    @pytest.mark.django_db
    def test_logout_view(self, client, users):
        user = users["user"]
        client.login(email=user.email, password=user.password)

        response = client.post(reverse("account:logout"))

        assert isinstance(response, HttpResponseRedirect)
        assert response.url == reverse("core:index")

    # Тесты для AccountSingUpView
    def test_signup_view_get_unauthenticated(self, factory, mocker):
        request = factory.get(reverse("account:signup"))
        request.user = mocker.Mock(is_authenticated=False)

        response = AccountSingUpView.as_view()(request)

        assert response.status_code == 200
        assert b"Sign Up" in response.content

    def test_signup_view_authenticated_redirect(self, factory, users):
        request = factory.get(reverse("account:signup"))
        request.user = users["user"]

        response = AccountSingUpView.as_view()(request)

        assert isinstance(response, HttpResponseRedirect)
        assert response.url == reverse("core:index")

    @pytest.mark.django_db
    def test_profile_detail_view(self, factory, users):
        user = users["user"]
        request = factory.get(
            reverse(
                "account:profile_detail",
                args={"slug": user.slug},
            ),
        )
        request.user = user

        response = AccountProfileDetailView.as_view()(request, slug=user.slug)

        assert response.status_code == 200
        assert "title" in response.context_data
        assert (
            response.context_data["title"] == f"Profile Details {user.username}"
        )
        assert response.context_data["profile"] == user

    # Тесты для AccountProfileUpdateView
    def test_profile_update_view_get(self, factory, users):
        user = users["user"]
        request = factory.get(
            reverse(
                "account:profile_edit",
                args={"slug": user.slug},
            ),
        )
        request.user = user

        response = AccountProfileUpdateView.as_view()(request)

        assert response.status_code == 200
        assert "title" in response.context_data
        assert response.context_data["title"] == f"Profile {user.username}"
        assert response.context_data["profile"] == user

    @pytest.mark.django_db
    def test_profile_update_view_post_valid(self, factory, users):
        user = users["user"]
        data = {"username": "newusername", "email": "user@test.com"}
        request = factory.post(
            reverse(
                "account:profile_edit",
                args={"slug": user.slug},
            ),
            data,
        )
        request.user = user

        response = AccountProfileUpdateView.as_view()(request)

        assert response.status_code == 302
        updated_user = Account.objects.get(id=user.id)
        assert updated_user.username == "newusername"
        assert updated_user.email == "user@test.com"

    @pytest.mark.django_db
    def test_password_reset_view_valid_email(self, client, mocker, users):

        data = {"email": users["user"].email}

        mock_send_email = mocker.patch(
            "app.account.tasks.send_reset_password_email.delay"
        )

        response = client.post(
            reverse("account:password_reset"), data, follow=False
        )

        assert response.status_code == 302
        assert response.url == reverse("account:password_reset_done")
        mock_send_email.assert_called_once_with("user@test.com")

    @pytest.mark.django_db
    def test_password_reset_view_invalid_email(self, client, mocker):
        data = {"email": ""}

        mock_send_email = mocker.patch(
            "app.account.tasks.send_reset_password_email.delay"
        )

        response = client.post(reverse("account:password_reset"), data)

        assert response.status_code == 200
        mock_send_email.assert_not_called()

    def test_password_reset_view_get(self, client):
        """Тест GET-запроса к странице сброса пароля."""
        response = client.get(reverse("account:password_reset"))

        assert response.status_code == 200
        assert "title" in response.context_data
        assert response.context_data["title"] == "Password reset"
        assert "form" in response.context_data

    def test_password_reset_done_view(self, client):
        """Тест страницы подтверждения отправки email."""
        response = client.get(reverse("account:password_reset_done"))

        assert response.status_code == 200
        assert "title" in response.context_data
        assert response.context_data["title"] == "Password Reset Done"

    @pytest.mark.django_db
    def test_password_reset_confirm_view_get_valid_token(
        self,
        client,
        users,
        mocker,
    ):
        """Тест GET-запроса с валидным токеном."""
        user = users["user"]
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse(
            "account:password_reset_confirm",
            args={"uidb64": uid, "token": token},
        )

        response = client.get(url)

        assert response.status_code == 200
        assert "title" in response.context_data
        assert response.context_data["title"] == "Password Reset Confirm"
        assert "form" in response.context_data

    @pytest.mark.django_db
    def test_password_reset_confirm_view_post_valid(self, client, users,
                                                    mocker):
        """Тест успешного сброса пароля с валидным токеном."""
        user = users["user"]
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse(
            "account:password_reset_confirm",
            kwargs={"uidb64": uid, "token": token},
        )
        data = {
            "new_password1": "newpass123",
            "new_password2": "newpass123",
        }
        response = client.post(url, data, follow=False)

        assert response.status_code == 302
        assert response.url == f"/account/password-reset/{uid}/set-password/"
        response = client.post(response.url, data, follow=False)
        user.refresh_from_db()
        assert user.check_password("newpass123")

    @pytest.mark.django_db
    def test_password_reset_confirm_view_invalid_token(
        self, client, users, mocker
    ):
        """Тест GET-запроса с невалидным токеном (краевой случай)."""
        user = users["user"]
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse(
            "account:password_reset_confirm",
            kwargs={"uidb64": uid, "token": "invalid-token"},
        )

        response = client.get(url)

        assert response.status_code == 200
        assert "title" in response.context_data
        assert (
            response.context_data["validlink"] is False
        )  # Ссылка недействительна

    @pytest.mark.django_db
    def test_password_reset_confirm_view_mismatched_passwords(self, client,
                                                              users, mocker):
        """Тест отправки формы с несовпадающими паролями (краевой случай)."""
        user = get_user_model().objects.create_user(
            email="newuser@test.com",
            password="test_password",
            username="newuser",
        )
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse(
            "account:password_reset_confirm",
            kwargs={"uidb64": uid, "token": token},
        )
        data = {
            "new_password1": "newpass123",
            "new_password2": "differentpass",
        }
        response = client.post(url, data, follow=False)

        assert response.status_code == 302
        response = client.post(response.url, data, follow=False)
        assert response.status_code == 200  # Ожидаем возврат формы
        assert "form" in response.context_data
        assert response.context_data["form"].errors  # Ошибки в форме
        user.refresh_from_db()
        assert not user.check_password("newpass123")  # Пароль не обновлен

    # Тесты для AccountPasswordResetCompleteView
    def test_password_reset_complete_view(self, client):
        """Тест страницы завершения сброса пароля."""
        response = client.get(reverse("account:password_reset_complete"))

        assert response.status_code == 200
        assert "title" in response.context_data
        assert response.context_data["title"] == "Password Reset Complete"

