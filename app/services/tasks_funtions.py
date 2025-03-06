# -*- coding: UTF-8 -*-
"""Utils functions for celery tasks."""
from typing import Callable

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

Account = get_user_model()


def generate_password_reset_uidb_and_token(user: Account) -> tuple[str, str]:
    """Generate uid and token for password reset.

    Args:
        user (Account): User object.

    Returns:
        Generated uid64 and token.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uidb64, token


def prepare_password_reset_email_letter(
        user: Account,
        email: str,
        uidb64: str,
        token: str,
        template_name: str,
) -> Callable:
    """Prepare password reset email message.

    Args:
        user (Account): User object.
        email (str): User's email address.
        uidb64 (str): User's uidb64.
        token (str): User's token.
        template_name (str): Template name.

    Returns:
        Rendered template with context data.
    """
    message = render_to_string(
        template_name=template_name,
        context={
            "email": email,
            "domain": settings.DOMAIN,
            "site_name": settings.SITE_NAME,
            "uidb64": uidb64,
            "user": user,
            "token": token,
            "protocol": "https" if settings.USE_HTTPS else "http",
        },
    )
    return message
