# -*- coding: UTF-8 -*-
"""This module adds custom forms for the `account` application."""
from typing import Optional

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)

from app.account.models import Account


class AccountLoginForm(forms.Form):
    """Form to log in a user."""

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput,
    )
    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput,
    )
    remember_me = forms.BooleanField(
        label="Remember me",
        required=False,
        initial=False,
        widget=forms.CheckboxInput,
    )

    class Meta:
        """The Class adds metadata options."""

        model = Account
        fields = ("email", "password", "remember_me")

    def __init__(self, *args, **kwargs):
        """Form initialization.

        Removed from kwargs request because it caused an error.

        Args:
            *args (tuple): Positional arguments.
            **kwargs (dict): Keyword arguments.
        """
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "",
                },
            )
        self.fields["remember_me"].widget.attrs.update(
            {
                "class": "form-check-input me-2",
            },
        )

    def get_user(self) -> Optional[Account]:
        """Authenticate user object.

        This method is not called until the form has been
        successfully validated.

        Returns:
            Account: Account instance.
        """
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(
            request=self.request,
            username=email,
            password=password,
            backend="app.account.backends.EmailAuthBackend",
        )
        return user

    def clean(self) -> None:
        """Perform validation that requires access to multiple form fields.

        Raises:
            ValidationError: if user not found or password isn't correct.
        """
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = Account.objects.filter(email=email).first()
        if not user:
            raise forms.ValidationError("Email isn't registered")
        if not user.check_password(password):
            raise forms.ValidationError("Email or password isn't correct")


class AccountSignUpForm(UserCreationForm):
    """Form to create a new user."""

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-check-input"}),
    )

    subscribe = forms.BooleanField(
        label="Subscribe to our newsletter",
        required=False,
    )

    class Meta:
        """The Class adds metadata options."""

        model = Account
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "subscribe",
        ]

    def __init__(self, *args, **kwargs):
        """Form initialization.

        Adds attributes to the bootstrap form element widget.

        Args:
            *args (tuple): Positional arguments.
            **kwargs (dict): Keyword arguments.
        """
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "",
                },
            )
        self.fields["subscribe"].widget.attrs.update(
            {
                "class": "form-check-input me-2",
            },
        )

    def clean(self) -> None:
        """Perform validation that requires access to multiple form fields.

        Raises:
            ValidationError: if passwords is mismatch.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords must match")


class AccountProfileUpdateForm(forms.ModelForm):
    """Form to update a user's profile."""

    class Meta:
        """The Class adds metadata options."""

        model = Account
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "avatar",
            "bio",
            "birth_day",
            "subscribe",
        ]

    def __init__(self, *args, **kwargs):
        """Form initialization.

        Adds attributes to the bootstrap form element widget.

        Args:
            *args (tuple): Positional arguments.
            **kwargs (dict): Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "",
                },
            )

        self.fields["subscribe"].widget.attrs.update(
            {
                "class": "form-check-input me-2",
            },
        )


class AccountPasswordChangeForm(PasswordChangeForm):
    """Form to update a user's password."""

    class Meta:
        """The Class adds metadata options."""

        model = Account
        fields = ["old_password", "new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        """Form initialization.

        Adds attributes to the bootstrap form element widget.

        Args:
            *args (tuple): Positional arguments.
            **kwargs (dict): Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "",
                },
            )


class AccountPasswordResetFrom(PasswordResetForm):
    """Form to change a user's password by email."""

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": ""},
        ),
    )

    def clean_email(self) -> str:
        """Validate that the email address is correct.

        Returns:
            If the email string is correct then it is returned,
            otherwise a ValidationError raise.

        Raises:
            ValidationError: if the email address isn't registered.
        """
        email = self.cleaned_data.get("email")
        user = Account.objects.filter(email=email).first()
        if not user:
            raise forms.ValidationError("Email isn't registered")
        return email


class AccountSetPasswordForm(SetPasswordForm):
    """Form to change a user's password by email.

    The form contains password1 and password2 as input fields.
    """

    def __init__(self, *args, **kwargs):
        """Form initialization.

        Adds attributes to the bootstrap form element widget.

        Args:
            *args (tuple): Positional arguments.
            **kwargs (dict): Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control mb-1", "placeholder": ""},
            )
