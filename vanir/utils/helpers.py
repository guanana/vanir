from django.core.exceptions import ValidationError

from vanir.token.models import Coin


def fetch_default_account():
    from vanir.account.models import Account

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


def value_pair(tkn: Coin, tkn2: Coin):
    return f"{tkn.symbol}{tkn2.symbol}"
