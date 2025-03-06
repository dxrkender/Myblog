# -*- coding: UTF-8 -*-
"""This module adds the custom authentication backend."""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest


class EmailAuthBackend(ModelBackend):
    """Authenticate against email address."""

    def authenticate(
            self,
            request: HttpRequest,
            username: str = None,
            password: str = None,
            **kwargs,
    ):
        """Authenticate method by email (username) and password.

        Args:
            request (HttpRequest): object that contains metadata about
                the request.
            username (str): it's actually an email because django uses
                username by default.
            password (str): password hash.
            **kwargs (dict): some extra keyword arguments.

        Returns:
            User if it exists and the correct password is provided,
            None otherwise.
        """
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, email: str):
        """User extraction method.

        Args:
            email (str): user email.

        Returns:
            User if it exists, None otherwise.
        """
        user_model = get_user_model()
        try:
            return user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return None
