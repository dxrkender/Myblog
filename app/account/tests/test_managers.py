import pytest
from django.core.exceptions import ValidationError
from app.account.models import Account  # Импортируйте модель Account


from app.tests.conftest import test_email, test_password


class TestAccountManager:

    @pytest.fixture
    def account_manager(self):
        return Account.objects

    @pytest.mark.django_db
    def test_create_user_success(
        self, account_manager, test_email, test_password
    ):
        """Test creating a regular user successfully."""
        # Создаем пользователя
        user = account_manager.create_user(
            email=test_email, password=test_password
        )

        # Проверяем, что пользователь создан корректно
        assert (
            user.email == test_email
        ), "User email should match the provided email"
        assert user.check_password(
            test_password
        ), "User password should be set correctly"
        assert user.is_active is True, "New users should be active by default"
        assert (
            user.is_staff is False
        ), "New users should not be staff by default"
        assert (
            user.is_superuser is False
        ), "New users should not be superusers by default"

    def test_create_user_no_email(self, account_manager, test_password):
        """Test creating a user without an email."""
        with pytest.raises(
            ValueError, match="Users must have an email address"
        ):
            account_manager.create_user(email=None, password=test_password)

    @pytest.mark.django_db
    def test_create_superuser(self, account_manager, test_email, test_password):
        """Test creating a superuser successfully."""
        # Создаем суперпользователя
        superuser = account_manager.create_superuser(
            email=test_email, password=test_password
        )

        # Проверяем, что суперпользователь создан корректно
        assert (
            superuser.email == test_email
        ), "Superuser email should match the provided email"
        assert superuser.check_password(
            test_password
        ), "Superuser password should be set correctly"
        assert (
            superuser.is_active is True
        ), "Superusers should be active by default"
        assert superuser.is_staff is True, "Superusers should be staff"
        assert (
            superuser.is_superuser is True
        ), "Superusers should have superuser status"
