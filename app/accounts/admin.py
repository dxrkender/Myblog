from django.contrib import admin

from app.accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    ...
