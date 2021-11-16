import logging

from django.conf import settings
from django.db.models import QuerySet

from vanir.core.account.models import Account, AccountTokens
from vanir.core.token.models import Token
from vanir.utils.exceptions import AccountRequiredError, ExchangeExtendedFunctionalityError
from vanir.utils.helpers import fetch_default_account, value_pair

logger = logging.getLogger(__name__)


def token_import(
    account: Account, token_symbol: str, token_fullname: str = None
) -> Token:
    try:
        if not token_fullname:
            token_fullname = account.exchange_obj.get_token_full_name(token_symbol)
        token_obj = Token.objects.get(symbol=token_symbol)
        if token_obj.name != token_fullname and not account.testnet:
            logger.info(
                f"Updating token name from {token_obj.name} to {token_fullname}"
            )
            token_obj.name = token_fullname
            token_obj.save()
    except Token.DoesNotExist:
        token_obj = Token.objects.create(name=token_fullname, symbol=token_symbol)
    return token_obj


def import_token_account(token_obj: Token, account: Account, quantity: float):
    try:
        account_token = AccountTokens.objects.get(account=account, token=token_obj)
    except AccountTokens.DoesNotExist:
        account_token = AccountTokens.objects.create(account=account, token=token_obj)
    account_token.quantity = quantity
    account_token.save()
    return token_obj


def token_update(token: Token, price_dict: dict):
    """
    Checks price for the token base on the dictionary with prices that
    gets as parameter
    :param token: Token to check and update
    :param price_dict: Price for ALL the tokens for the exchange
    """
    symboltopair = settings.VANIR_BASE_SYSTEM_PAIR
    pair = value_pair(token, symboltopair.upper())
    try:
        token.last_value = price_dict[pair]
    except KeyError:
        try:
            # If it's USD try to see if USDT is in the list
            if symboltopair == "USD":
                pair = value_pair(token, f"{symboltopair.upper()}T")
                token.last_value = price_dict[pair]
        except KeyError:
            if pair == "SAME_TOKEN":
                token.last_value = 1
            else:
                token.last_value = catch_ld_binance(token, price_dict)
    token.save()


def catch_ld_binance(token: Token, price_dict: dict):
    """
    Last try to see if it's special type Binance LD<TOKEN>
    :param token: Token to check and update
    :param price_dict: Price for ALL the tokens for the exchange
    :return: price
    :rtype: float
    """
    symboltopair = settings.VANIR_BASE_SYSTEM_PAIR
    try:
        if token.symbol[2:].upper() in {symboltopair.upper(), f"{symboltopair.upper()}T"}:
            return 1
        pair = value_pair(token, f"{symboltopair.upper()}")
        pair = pair[2:]
        return price_dict[pair]
    except KeyError:
        try:
            pair = value_pair(token, f"{symboltopair.upper()}T")
            pair = pair[2:]
            return price_dict[pair]
        except KeyError:
            return float(0)


def qs_update(token_qs: QuerySet[Token], account: Account = None):
    if not account:
        account = fetch_default_account()
    price_dict = account.exchange_obj.all_assets_prices
    for token in token_qs:
        token_update(token.token, price_dict)
        token.save()


def bulk_update(account: Account = None):
    if not account:
        account = fetch_default_account()
        if not account:
            raise AccountRequiredError
    try:
        price_dict = account.exchange_obj.all_assets_prices
    except AttributeError:
        raise ExchangeExtendedFunctionalityError
    for token_obj in Token.objects.all():
        token_update(token_obj, price_dict)
