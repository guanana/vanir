from django.core.exceptions import ValidationError

from vanir.core.exchange.libs.exchanges import ExtendedExchangeRegistry
from vanir.core.token.models import Coin
from vanir.utils.exceptions import ExchangeExtendedFunctionalityError


def fetch_default_account():
    """
    Fetch default account from all the accounts
    :return: default account
    :rtype: Account
    """
    from vanir.core.account.models import Account

    if Account.objects.count() == 0:
        return None
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


def fetch_exchange_obj(exchange_name: str):
    """
    Check for registry in Extended exchange and returns
    the exchange class
    :return: Exchange object
    :rtype: BasicExchange
    """
    try:
        class_obj = ExtendedExchangeRegistry.get_class_by_name(
            exchange_name.split(" ")[0]
        )
    except KeyError:
        raise ExchangeExtendedFunctionalityError(
            f"Please create an account with a supported Exchange to get extra functionalities"
            f"{[item for item in ExtendedExchangeRegistry.registered.keys()]}"
        )
    return class_obj


def value_pair(tkn: Coin, tkn2: str = "USDT"):
    return f"{tkn.symbol}{tkn2}"
