import pytest

from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from app.account.models import Account


class TestAccountModel:

    @pytest.fixture
    def full_account(self):
        return Account(
            email="test@test.com",
            username="testuser",
            slug="testuser",
            password="test_password123",
            bio="A short biography",
            birth_day=now().date(),
            subscribe=True,
            confirm_email=True,
        )

    def test_fields_definition(self):
        """Test the definition of fields in the model."""
        account = Account(email="test@test.com", username="testuser")

        assert isinstance(
            account._meta.get_field("email"), models.EmailField
        ), "Email field should be EmailField"
        assert isinstance(
            account._meta.get_field("slug"), models.SlugField
        ), "Slug field should be SlugField"
        assert isinstance(
            account._meta.get_field("avatar"), models.ImageField
        ), "Avatar field should be ImageField"
        assert isinstance(
            account._meta.get_field("bio"), models.TextField
        ), "Bio field should be TextField"
        assert isinstance(
            account._meta.get_field("birth_day"), models.DateField
        ), "Birth Day field should be DateField"
        assert isinstance(
            account._meta.get_field("subscribe"), models.BooleanField
        ), "Subscribe field should be BooleanField"
        assert isinstance(
            account._meta.get_field("confirm_email"), models.BooleanField
        ), "Confirm Email field should be BooleanField"

        assert (
            account._meta.get_field("email").unique is True
        ), "Email field should be unique"
        assert (
            account._meta.get_field("slug").unique is True
        ), "Slug field should be unique"

        assert (
            account._meta.get_field("username").max_length == 255
        ), "Username field max length should be 255"
        assert (
            account._meta.get_field("email").max_length == 255
        ), "Email field max length should be 255"

    def test_str_method(self, full_account):
        """Test the __str__ method."""
        assert (
            str(full_account) == "test@test.com"
        ), "String representation should be the email address"

    def test_get_absolute_url(self, full_account):
        """Test the get_absolute_url method."""
        full_account.slug = "test-slug"
        url = full_account.get_absolute_url()
        assert (
            url == "/account/profile/test-slug/"
        ), "URL should match the expected pattern"

    @pytest.mark.django_db
    def test_save_method_generates_slug(self, full_account):
        """Test that the save method generates a unique slug."""
        user = Account(
            email="test2@test.com",
            username="testuser",
            password="test_password123"
        )
        assert not user.slug, "Slug should be empty before saving"

        user.save()

        assert user.slug, "Slug should be generated after saving"

    @pytest.mark.django_db
    def test_avatar_file_extension_validation(self, full_account):
        """Test the avatar file extension validation."""
        full_account.avatar = "invalid.txt"
        with pytest.raises(ValidationError, match="File extension"):
            full_account.full_clean()

        full_account.avatar = "valid.jpg"
        try:
            full_account.full_clean()
        except ValidationError:
            pytest.fail(
                "Valid file extension should not raise a validation error"
            )

    def test_meta_class(self):
        """Test the Meta class."""
        meta = Account._meta

        assert (
            meta.verbose_name == "Account"
        ), "Verbose name should be 'Account'"
        assert (
            meta.verbose_name_plural == "Accounts"
        ), "Verbose name plural should be 'Accounts'"
        assert (
            meta.app_label == "app_account"
        ), "App label should be 'app_account'"

    def test_username_uniqueness(self, db):
        """Test that the username is not unique."""
        Account.objects.create_user(
            email="user1@test.com", username="testuser", password="password123"
        )

        with pytest.raises(
            ValueError, match="Users must have an email address"
        ):
            Account.objects.create_user(
                email=None, username="testuser", password="password123"
            )

        second_user = Account.objects.create_user(
            email="user2@test.com", username="testuser", password="password123"
        )
        assert (
            second_user.username == "testuser"
        ), "Username should not be unique"

    def test_email_unique(self, db):
        """Test that the email is unique."""
        Account.objects.create_user(
            email="user1@test.com", username="user1", password="password123"
        )

        with pytest.raises(
            IntegrityError,
            match="UNIQUE constraint failed: app_account_account.email",
        ):
            Account.objects.create_user(
                email="user1@test.com", username="user2", password="password123"
            )
