# -*- coding: UTF-8 -*-
"""This module adds config for the `account` application."""
from django.apps import AppConfig


class AccountConfig(AppConfig):
    """Class representing an `account` application and its configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.account'
    label = 'app_account'
