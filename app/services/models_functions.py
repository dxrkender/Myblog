# -*- coding: UTF-8 -*-
"""This module provides utility functions for models."""
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.utils.functional import lazy
from pytils.translit import slugify

Account = lazy(get_user_model, object)()


def unique_slugify(instance: Account, slug: str) -> str:
    """Create a unique slug.

    Create a unique slug based on default slug functions.
    Until a unique slug is found, generation will occur.

    Args:
        instance (Account): Account instance.
        slug (str): Base slug string.

    Returns:
        Unique slug string.
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        suffix = uuid4().hex[:8]
        unique_slug = f"{slugify(slug)}-{suffix}"
    return unique_slug
