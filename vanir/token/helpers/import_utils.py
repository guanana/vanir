from django.db.models import QuerySet

from vanir.account.models import Account
from vanir.account.models_relation import AccountTokens
from vanir.blockchain.models import Blockchain
from vanir.token.models import Token
from vanir.utils.helpers import fetch_default_account, value_pair


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
    account: Account, token: str, quantity: float = None, blockchain: Blockchain = None
) -> Token:
    if not blockchain:
        blockchain = account.exchange_obj.default_blockchain
    token_obj, token_created = Token.objects.get_or_create(
        name=get_token_full_name(account, token), symbol=token, blockchain=blockchain
    )
    if quantity:
        AccountTokens(account=account, token=token_obj, quantity=quantity).save()
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
    price_dict = account.exchange_obj.all_assets_prices
    for token_obj in Token.objects.all():
        token_update(token_obj, account, price_dict)
