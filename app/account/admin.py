# -*- coding: UTF-8 -*-
"""This module customizes admin UI for the `account` application."""
from django.contrib import admin

from app.account.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Custom admin for Account in Django Admin."""

    empty_value_display = "None"
    list_display = (
        "first_name",
        "last_name",
        "username",
        "email",
    )
    search_fields = ("username", "email")
