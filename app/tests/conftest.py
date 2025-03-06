import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from app.account.forms import AccountLoginForm


@pytest.fixture(scope="function")
def users(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = get_user_model().objects.create_user(
            email="user@test.com", password="test_password", username="user"
        )
        admin = get_user_model().objects.create_user(
            email="admin@test.com", password="test_password", username="admin"
        )
        users = {
            "user": user,
            "admin": admin,
        }
    yield users
    with django_db_blocker.unblock():
        user.delete()
        admin.delete()


@pytest.fixture(scope="session")
def account():
    Account = get_user_model()
    account = Account(email="test@test.com", username="user")
    account.set_password("test_password")
    return account


@pytest.fixture(scope="function")
def account_login_form_with_request():
    return AccountLoginForm(
        data={
            "email": "user@test.com",
            "password": "test_password",
            "remember_me": False,
        },
        request={"some_key": "some_value"},
    )


@pytest.fixture
def test_email():
    return "test@test.com"


@pytest.fixture
def test_password():
    return "test_password"


@pytest.fixture
def factory():
    """Фикстура для создания RequestFactory."""
    return RequestFactory()
