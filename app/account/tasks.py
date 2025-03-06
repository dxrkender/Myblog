# -*- coding: UTF-8 -*-
"""Tasks module for celery in `account` application."""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from app.myblog import celery_app
from app.services.tasks_funtions import (
    generate_password_reset_uidb_and_token,
    prepare_password_reset_email_letter,
)

Account = get_user_model()


@celery_app.task
def send_reset_password_email(email) -> None:
    """Celery task for sending password reset email.

    Args:
        email (str): User's email address.
    """
    user = Account.objects.get(email=email)
    uidb64, token = generate_password_reset_uidb_and_token(user)
    message = prepare_password_reset_email_letter(
        user=user,
        email=email,
        uidb64=uidb64,
        token=token,
        template_name="account/password_reset_email.html",
    )
    subject = "Myblog Password Reset"
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
