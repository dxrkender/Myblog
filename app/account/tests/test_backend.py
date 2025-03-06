import pytest
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from app.tests.conftest import users
from app.account.backends import EmailAuthBackend
from app.account.models import Account


@pytest.mark.django_db
def test_email_auth_backend_authenticate(users):
    """Testing EmailAuthBackend, authenticate method."""

    assert authenticate(
        email=users["user"].email,
        password="test_password",
        backend=EmailAuthBackend,
    ), "Correct user isn't authenticated"

    assert (
        authenticate(
            email=users["user"].email,
            password="wrong_password",
            backend=EmailAuthBackend,
        )
        is None
    ), "Wrong user is authenticated"

    assert (
        authenticate(
            email="fake@email.com",
            password="wrong_password",
            backend=EmailAuthBackend,
        )
        is None
    ), "Fake user is authenticated"


@pytest.mark.django_db
def test_email_auth_backend_get_user(users):
    """ Testing EmailAuthBackend, get_user method."""

    assert users["user"] == EmailAuthBackend().get_user(users["user"].email), \
        "User matches"

    assert users["user"] != EmailAuthBackend().get_user("fake@email.com"), \
        "User doesn't match"
