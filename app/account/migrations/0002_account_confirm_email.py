# Generated by Django 5.1.6 on 2025-02-25 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="confirm_email",
            field=models.BooleanField(
                default=False, verbose_name="Confirm Email"
            ),
        ),
    ]
