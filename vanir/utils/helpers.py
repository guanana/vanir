from django.core.exceptions import ValidationError

from vanir.account.models import Account


def change_table_style(table_html, html_class="text-center thead-light"):
    return table_html.replace("<thead>", f"<thead class='{html_class}>'")


def change_table_align(table_html, align="center"):
    return table_html.replace("text-align: right;", f"text-align: {align};")


def fetch_default_account() -> Account:
    account = [account for account in Account.objects.all() if account.default]
    if not account:
        if Account.objects.count() > 0:
            raise ValidationError(
                "At least one account should be default, please fix that!"
            )
        else:
            return None
    if len(account) > 1:
        raise ValidationError(
            "More than one account is labeled as default, please correct that first!"
        )
    return account[0]
