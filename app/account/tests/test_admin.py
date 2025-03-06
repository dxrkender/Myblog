from app.account.admin import AccountAdmin


def test_account_admin_attributes():
    assert AccountAdmin.empty_value_display == "None", \
        "empty_value_display isn't correct"
    assert AccountAdmin.list_display == (
        "first_name",
        "last_name",
        "username",
        "email",
    ), "list_display isn't correct"
    assert AccountAdmin.search_fields == ("username", "email"), \
        "search_fields isn't correct"
