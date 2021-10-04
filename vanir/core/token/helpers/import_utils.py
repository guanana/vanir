import logging

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from vanir.core.account.models import Account, AccountTokens
from vanir.core.token.models import Token
from vanir.utils.helpers import fetch_default_account, value_pair

logger = logging.getLogger(__name__)


def get_token_full_name(account: Account, token_symbol: str) -> str:
    if not account.testnet:
        try:
            name = account.exchange_obj.all_margin_assets[token_symbol]
        except KeyError:
            name = token_symbol
    else:
        name = token_symbol
    return name


def token_import(
    account: Account, token_symbol: str, token_fullname: str = None
) -> Token:
    try:
        if not token_fullname:
            token_fullname = get_token_full_name(account, token_symbol)
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


def token_update(token: Token, account: Account, price_dict: dict):
    pair = value_pair(token, account.token_pair)
    try:
        token.last_value = price_dict[pair]
        token.save()
    except KeyError:
        token.last_value = 0
        token.save()


def qs_update(token_qs: QuerySet[Token], account: Account = None):
    if not account:
        account = fetch_default_account()
    price_dict = account.exchange_obj.all_assets_prices
    for token in token_qs:
        token_update(token.token, account, price_dict)
        token.save()


def bulk_update(account: Account = None):
    if not account:
        account = fetch_default_account()
        if not account:
            raise ValidationError("You need to have at least one account configured")
    price_dict = account.exchange_obj.all_assets_prices
    for token_obj in Token.objects.all():
        token_update(token_obj, account, price_dict)
