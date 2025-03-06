# -*- coding: UTF-8 -*-
"""Creating models for the `account` application."""
from typing import Callable

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.shortcuts import reverse

from app.account.managers import AccountManager
from app.services.models_functions import unique_slugify


class Account(AbstractUser):
    """Blog user model."""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    DEFAULT_LENGTH_FIELD = 255

    username = models.CharField(
        unique=False,
        max_length=DEFAULT_LENGTH_FIELD,
    )

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        max_length=DEFAULT_LENGTH_FIELD,
        null=False,
        blank=False,
    )

    slug = models.SlugField(unique=True, verbose_name="Slug")
    avatar = models.ImageField(
        verbose_name="Avatar",
        default="images/avatars/default.png",
        upload_to="images/avatars/%Y/%m/%d/",
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg"]),
        ],
    )
    bio = models.TextField(verbose_name="Bio", blank=True, null=True)
    birth_day = models.DateField(
        verbose_name="Birth Day",
        blank=True,
        null=True,
    )
    subscribe = models.BooleanField(
        verbose_name="Subscribe to our newsletter",
        default=False,
    )

    objects = AccountManager()

    confirm_email = models.BooleanField(
        verbose_name="Confirm Email",
        default=False,
    )

    class Meta:
        """The Class adds metadata options."""

        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        app_label = "app_account"

    def __str__(self) -> str:
        """Introduce user via email because it is unique.

        Returns:
            String representation of the user.
        """
        return self.email

    def get_absolute_url(self) -> Callable:
        """Calculate the canonical URL of an object.

        Returns:
            Callable: URL of the object by self slug.
        """
        return reverse("account:profile_detail", args=(self.slug,))

    def save(self, *args, **kwargs) -> None:
        """Save the account to the database and add unique slug to the user.

        Args:
            *args (tuple): Positional arguments.
            **kwargs (dict): Keyword arguments.
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.username)
        super().save(*args, **kwargs)
