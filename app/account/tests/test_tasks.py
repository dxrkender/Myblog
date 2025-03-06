import pytest
from app.account.tasks import send_reset_password_email
from django.conf import settings


class TestSendResetPasswordEmailTask:
    def test_send_reset_password_email(self, mocker):
        """Test the send_reset_password_email Celery task."""
        mock_user = mocker.MagicMock()
        mock_user.email = "test@test.com"
        mock_user_get = mocker.patch("app.account.tasks.Account.objects.get")
        mock_user_get.return_value = mock_user

        mock_generate_token = mocker.patch(
            "app.account.tasks.generate_password_reset_uidb_and_token"
        )
        mock_generate_token.return_value = ("mock_uidb64", "mock_token")

        mock_prepare_email = mocker.patch(
            "app.account.tasks.prepare_password_reset_email_letter"
        )
        mock_prepare_email.return_value = "This is a mock email message"

        mock_send_mail = mocker.patch("app.account.tasks.send_mail")

        # Вызываем задачу
        send_reset_password_email("test@test.com")

        mock_user_get.assert_called_once_with(email="test@test.com")

        mock_generate_token.assert_called_once_with(mock_user)

        mock_prepare_email.assert_called_once_with(
            user=mock_user,
            email="test@test.com",
            uidb64="mock_uidb64",
            token="mock_token",
            template_name="account/password_reset_email.html",
        )

        mock_send_mail.assert_called_once_with(
            subject="Myblog Password Reset",
            message="This is a mock email message",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=["test@test.com"],
        )
