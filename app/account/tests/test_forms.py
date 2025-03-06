import pytest
from django import forms
from django.core.exceptions import ValidationError

from app.account.forms import (
    AccountLoginForm,
    AccountProfileUpdateForm,
    AccountPasswordChangeForm,
    AccountPasswordResetFrom,
    AccountSignUpForm,
)
from app.account.models import Account
from app.tests.conftest import account, account_login_form_with_request, users


class TestAccountLoginForm:

    def test_form_field_labels(self):
        """Test that the labels of the form fields are correct."""
        form = AccountLoginForm()
        assert (
            form.fields["email"].label == "Email"
        ), "Incorrect label for email field"
        assert (
            form.fields["password"].label == "Password"
        ), "Incorrect label for password field"
        assert (
            form.fields["remember_me"].label == "Remember me"
        ), "Incorrect label for remember_me field"

    def test_form_field_required(self):
        """Test that the required fields are correctly set."""
        form = AccountLoginForm()
        assert (
            form.fields["email"].required is True
        ), "Email field should be required"
        assert (
            form.fields["password"].required is True
        ), "Password field should be required"
        assert (
            form.fields["remember_me"].required is False
        ), "Remember_me field should not be required"

    def test_form_field_widgets(self):
        """Test that the correct widgets are used for each field."""
        form = AccountLoginForm()
        assert isinstance(
            form.fields["email"].widget, forms.EmailInput
        ), "Email field should use EmailInput widget"
        assert isinstance(
            form.fields["password"].widget, forms.PasswordInput
        ), "Password field should use PasswordInput widget"
        assert isinstance(
            form.fields["remember_me"].widget, forms.CheckboxInput
        ), "Remember_me field should use CheckboxInput widget"

    def test_form_field_widget_attrs(self):
        """Test that the attributes of the widgets are correctly set."""
        form = AccountLoginForm()
        email_attrs = form.fields["email"].widget.attrs
        password_attrs = form.fields["password"].widget.attrs
        remember_me_attrs = form.fields["remember_me"].widget.attrs

        assert (
            email_attrs.get("class") == "form-control"
        ), "Email field should have 'form-control' class"
        assert (
            email_attrs.get("placeholder") == ""
        ), "Email field should have an empty placeholder"

        assert (
            password_attrs.get("class") == "form-control"
        ), "Password field should have 'form-control' class"
        assert (
            password_attrs.get("placeholder") == ""
        ), "Password field should have an empty placeholder"

        assert (
            remember_me_attrs.get("class") == "form-check-input me-2"
        ), "Remember_me field should have 'form-check-input' class"

    def test_form_meta_class(self):
        """Test that the Meta class is correctly defined."""
        form = AccountLoginForm()
        meta = getattr(form, "Meta", None)
        assert meta is not None, "Metaclass should be defined"

        assert hasattr(
            meta, "model"
        ), "Metaclass should contain 'model' attribute"
        assert hasattr(
            meta, "fields"
        ), "Metaclass should contain 'fields' attribute"

        assert (
            meta.model.__name__ == "Account"
        ), "Model in Meta should be 'Account'"
        assert meta.fields == (
            "email",
            "password",
            "remember_me",
        ), "Fields in Meta should include 'email', 'password',\
         and 'remember_me'"

    def test_init_method(self):
        """Test the __init__ method of AccountLoginForm."""
        request_data = {"some_key": "some_value"}
        form = AccountLoginForm(request=request_data)

        assert (
            form.request == request_data
        ), "Request should be set correctly in the form instance"

        assert hasattr(form, "fields"), "Form fields should be initialized"

    def test_get_user_method_success(
        self, account_login_form_with_request, account, mocker
    ):
        """Test the get_user method when authentication is successful."""

        mock_filter = mocker.patch("app.account.models.Account.objects.filter")
        mock_filter.return_value.first.return_value = account

        mock_get = mocker.patch("app.account.models.Account.objects.get")
        mock_get.return_value = account

        account_login_form_with_request.is_valid()

        result = account_login_form_with_request.get_user()

        assert (
            result == account
        ), "get_user should return the authenticated user"
        assert (
            result.email == "test@test.com"
        ), "User email should match the provided email"

    def test_get_user_method_failure(
        self,
        account,
        account_login_form_with_request,
        mocker,
    ):
        """Test the get_user method when authentication fails."""
        mock_get = mocker.patch("app.account.models.Account.objects.get")
        mock_get.return_value = account

        account_login_form_with_request.cleaned_data = {
            "email": "user@test.com",
            "password": "fake_password",
        }

        result = account_login_form_with_request.get_user()
        assert (
            result is None
        ), "get_user should return None when authentication fails."

    def test_clean_email_not_registered(
        self,
        account_login_form_with_request,
        account,
        mocker,
    ):
        """Test the clean method when the email is not registered."""

        mock_filter = mocker.patch("app.account.models.Account.objects.filter")
        mock_filter.return_value.first.return_value = None

        with pytest.raises(ValidationError, match="Email isn't registered"):
            account_login_form_with_request.is_valid()
            account_login_form_with_request.clean()

    def test_clean_incorrect_password(
        self,
        account,
        account_login_form_with_request,
        mocker,
    ):
        """Test the clean method when the password is incorrect."""
        mock_filter = mocker.patch("app.account.models.Account.objects.filter")
        mock_filter.return_value.first.return_value = account

        account_login_form_with_request.data["password"] = "wrong_password"
        account_login_form_with_request.is_valid()

        with pytest.raises(
            ValidationError, match="Email or password isn't correct"
        ):
            account_login_form_with_request.is_valid()
            account_login_form_with_request.clean()

    def test_clean_success(
        self,
        account,
        account_login_form_with_request,
        mocker,
    ):
        """Test the clean method when the email and password are correct."""
        mock_filter = mocker.patch("app.account.models.Account.objects.filter")
        mock_filter.return_value.first.return_value = account

        account_login_form_with_request.is_valid()

        assert (
            account_login_form_with_request.clean() is None
        ), "Wrong clean method"


class TestAccountSignUpForm:

    def test_field_labels(self):
        """Test that the labels of the form fields are correct."""
        form = AccountSignUpForm()
        assert (
            form.fields["email"].label == "Email"
        ), "Incorrect label for email field"
        assert (
            form.fields["subscribe"].label == "Subscribe to our newsletter"
        ), "Incorrect label for subscribe field"

    def test_field_required(self):
        """Test that required fields are correctly set."""
        form = AccountSignUpForm()
        assert (
            form.fields["email"].required is True
        ), "Email field should be required"
        assert (
            form.fields["subscribe"].required is False
        ), "Subscribe field should not be required"

    def test_field_widgets(self):
        """Test that the correct widgets are used for each field."""
        form = AccountSignUpForm()
        assert isinstance(
            form.fields["email"].widget, forms.EmailInput
        ), "Email field should use EmailInput widget"
        assert isinstance(
            form.fields["subscribe"].widget, forms.CheckboxInput
        ), "Subscribe field should use CheckboxInput widget"

    def test_field_widget_attrs(self):
        """Test that the attributes of the widgets are correctly set."""
        form = AccountSignUpForm()
        for field_name in [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]:
            attrs = form.fields[field_name].widget.attrs
            assert (
                attrs.get("class") == "form-control"
            ), f"{field_name} field should have 'form-control' class"
            assert (
                attrs.get("placeholder") == ""
            ), f"{field_name} field should have an empty placeholder"

        subscribe_attrs = form.fields["subscribe"].widget.attrs
        assert (
            subscribe_attrs.get("class") == "form-check-input me-2"
        ), "Subscribe field should have 'form-check-input me-2' class"

    def test_meta_class(self):
        """Test that the Meta class is correctly defined."""
        form = AccountSignUpForm()
        meta = getattr(form, "Meta", None)
        assert meta is not None, "Metaclass should be defined"

        assert (
            meta.model.__name__ == "Account"
        ), "Model in Meta should be 'Account'"

        expected_fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "subscribe",
        ]
        assert (
            meta.fields == expected_fields
        ), "Fields in Meta should match the expected list"

    def test_clean_method_success(self, mocker):
        """Test the clean method when passwords match."""
        form = AccountSignUpForm(
            data={
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "john.doe@example.com",
                "password1": "test_password123",
                "password2": "test_password123",
                "subscribe": False,
            },
        )

        mock_account = mocker.patch("app.account.models.Account.objects.filter")
        mock_account.return_value.exists.return_value = False

        is_valid = form.is_valid()
        assert is_valid is True, "Form should be valid when passwords match"

    def test_clean_method_failure(self, mocker):
        """Test the clean method when passwords do not match."""
        form = AccountSignUpForm(
            data={
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "john.doe@example.com",
                "password1": "test_password123",
                "password2": "wrong_password",  # Пароли не совпадают
                "subscribe": False,
            }
        )

        mock_account = mocker.patch("app.account.models.Account.objects.filter")
        mock_account.return_value.exists.return_value = False

        with pytest.raises(ValidationError, match="Passwords must match"):
            form.is_valid()
            form.clean()


class TestAccountProfileUpdateForm:

    def test_meta_class(self):
        """Test that the Meta class is correctly defined."""
        form = AccountProfileUpdateForm()
        meta = getattr(form, "Meta", None)
        assert meta is not None, "Metaclass should be defined"

        assert (
            meta.model.__name__ == "Account"
        ), "Model in Meta should be 'Account'"

        expected_fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "avatar",
            "bio",
            "birth_day",
            "subscribe",
        ]
        assert (
            meta.fields == expected_fields
        ), "Fields in Meta should match the expected list"

    def test_init_method(self):
        """Test the __init__ method to ensure widget attributes are updated."""
        form = AccountProfileUpdateForm()

        for field_name in [
            "first_name",
            "last_name",
            "username",
            "email",
            "bio",
            "birth_day",
        ]:
            attrs = form.fields[field_name].widget.attrs
            assert (
                attrs.get("class") == "form-control"
            ), f"{field_name} field should have 'form-control' class"
            assert (
                attrs.get("placeholder") == "",
                f"{field_name} field should have empty placeholder"
            )

        subscribe_attrs = form.fields["subscribe"].widget.attrs
        assert (
            subscribe_attrs.get("class") == "form-check-input me-2"
        ), "Subscribe field should have 'form-check-input me-2' class"

    def test_field_required(self):
        """Test that required fields are correctly set."""
        form = AccountProfileUpdateForm()

        assert (
            form.fields["first_name"].required is False
        ), "First name field should not be required"
        assert (
            form.fields["last_name"].required is False
        ), "Last name field should not be required"
        assert (
            form.fields["username"].required is True
        ), "Username field should be required"
        assert (
            form.fields["email"].required is True
        ), "Email field should be required"
        assert (
            form.fields["avatar"].required is False
        ), "Avatar field should not be required"
        assert (
            form.fields["bio"].required is False
        ), "Bio field should not be required"
        assert (
            form.fields["birth_day"].required is False
        ), "Birth day field should not be required"
        assert (
            form.fields["subscribe"].required is False
        ), "Subscribe field should not be required"

    def test_field_labels(self):
        """Test that the labels of the form fields are correct."""
        form = AccountProfileUpdateForm()

        assert (
            form.fields["first_name"].label == "First name"
        ), "Incorrect label for first_name field"
        assert (
            form.fields["last_name"].label == "Last name"
        ), "Incorrect label for last_name field"
        assert (
            form.fields["username"].label == "Username"
        ), "Incorrect label for username field"
        assert (
            form.fields["email"].label == "Email"
        ), "Incorrect label for email field"
        assert (
            form.fields["avatar"].label == "Avatar"
        ), "Incorrect label for avatar field"
        assert (
            form.fields["bio"].label == "Bio"
        ), "Incorrect label for bio field"
        assert (
            form.fields["birth_day"].label == "Birth Day"
        ), "Incorrect label for birth_day field"
        assert (
            form.fields["subscribe"].label == "Subscribe to our newsletter"
        ), "Incorrect label for subscribe field"


class TestAccountPasswordChangeForm:

    def test_assert(self):
        assert 1 == 1

    def test_meta_class(self, account):
        """Test that the Meta class is correctly defined."""
        form = AccountPasswordChangeForm(account)
        meta = getattr(form, "Meta", None)
        assert meta is not None, "Metaclass should be defined"
        assert (
            meta.model.__name__ == "Account"
        ), "Model in Meta should be 'Account'"
        expected_fields = ["old_password", "new_password1", "new_password2"]
        assert (
            meta.fields == expected_fields
        ), "Fields in Meta should match the expected list"

    def test_field_widget_attrs(self, account):
        """Test that the attributes of the widgets are correctly set."""
        form = AccountPasswordChangeForm(account)

        for field_name in ["old_password", "new_password1", "new_password2"]:
            attrs = form.fields[field_name].widget.attrs
            assert (
                attrs.get("class") == "form-control"
            ), f"{field_name} field should have 'form-control' class"
            assert (
                attrs.get("placeholder") == ""
            ), f"{field_name} field should have an empty placeholder"


class TestAccountPasswordResetForm:

    def test_field_label(self):
        """Test that the label of the email field is correct."""
        form = AccountPasswordResetFrom()
        assert (
            form.fields["email"].label == "Email"
        ), "Incorrect label for email field"

    def test_field_required(self):
        """Test that the email field is required."""
        form = AccountPasswordResetFrom()
        assert (
            form.fields["email"].required is True
        ), "Email field should be required"

    def test_field_widget(self):
        """Test that the correct widget is used for the email field."""
        form = AccountPasswordResetFrom()
        assert isinstance(
            form.fields["email"].widget, forms.EmailInput
        ), "Email field should use EmailInput widget"

    def test_field_widget_attrs(self):
        """Test that the attributes of the email widget are correctly set."""
        form = AccountPasswordResetFrom()
        attrs = form.fields["email"].widget.attrs
        assert (
            attrs.get("class") == "form-control"
        ), "Email field should have 'form-control' class"
        assert (
            attrs.get("placeholder") == ""
        ), "Email field should have an empty placeholder"

    def test_clean_email_success(self, account, mocker):
        """Test the clean_email method when the email is registered."""
        mock_filter = mocker.patch("app.account.models.Account.objects.filter")
        mock_filter.return_value.first.return_value = account
        form = AccountPasswordResetFrom(data={"email": "user@test.com"})

        is_valid = form.is_valid()
        assert (
            is_valid is True
        ), "Form should be valid when the email is registered"

        cleaned_email = form.cleaned_data['email']
        assert (
            cleaned_email == "user@test.com"
        ), "Cleaned email should match the provided email"

        mock_filter.assert_called_once_with(email="user@test.com")

    def test_clean_email_failure(self, mocker):
        """Test the clean_email method when the email isn't registered."""
        mock_filter = mocker.patch("app.account.models.Account.objects.filter")
        mock_filter.return_value.first.return_value = None

        form = AccountPasswordResetFrom(data={"email": "fake@test.com"})
        form.cleaned_data = {"email": "fake@test.com"}

        with pytest.raises(ValidationError, match="Email isn't registered"):
            form.clean_email()

        mock_filter.assert_called_once_with(email="fake@test.com")
