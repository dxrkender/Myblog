# -*- coding: UTF-8 -*-
"""Define the custom manager class."""
from typing import Self

from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from django.utils.functional import lazy

Account = lazy(get_user_model, object)()


class AccountManager(BaseUserManager):
    """The account model manager.

    The class provides email authentication functionality.
    """

    def create_user(
        self,
        email: str,
        password: str = None,
        **extra_fields,
    ) -> Account:
        """Create and save a user with the given email and password.

        Args:
            email (str):  The email address of the user.
            password (str): The password for the user.
            **extra_fields (dict): Key-value pairs of user attributes.

        Raises:
            ValueError: If the email address registered.

        Returns:
            Account: The created user.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str = None,
        **extra_fields,
    ) -> Self:
        """Create superuser.

        Create a superuser with the specified email address and password,
        and add superuser attributes to it.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.
            **extra_fields (dict): Key-value pairs of user attributes.

        Returns:
            Create user with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, password=password, **extra_fields)
