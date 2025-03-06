from django.apps import apps
from django.conf import settings

from app.account.apps import AccountConfig


class TestAccountConfig:

    def test_account_config_default_auto_field(self):
        """Check that default_auto_field has the correct value."""
        assert AccountConfig.default_auto_field == "django.db.models.BigAutoField"

    def test_account_config_name(self):
        """Check that name has the correct value."""
        assert AccountConfig.name == "app.account"

    def test_account_config_label(self):
        """Check that label has the correct value."""
        assert AccountConfig.label == "app_account"

    def test_account_config_loaded(self):
        """Check that application is correct."""
        app_config = apps.get_app_config("app_account")
        assert isinstance(app_config, AccountConfig)
        assert app_config.name == "app.account"
        assert app_config.label == "app_account"
