from vanir.account.models import Account
from vanir.account.models_relation import AccountTokens
from vanir.account.utils import get_exchange
from vanir.blockchain.models import Blockchain
from vanir.token.models import Token


def get_token_full_name(account: Account, token_symbol):
    exchange_obj = get_exchange(account.exchange.pk)
    token_dict = exchange_obj.get_all_assets()
    try:
        name = token_dict[token_symbol]
    except KeyError:
        name = token_symbol
    return name


def token_import(
    account: Account, token: str, quantity: int = None, blockchain: Blockchain = None
):
    if not blockchain:
        blockchain = get_exchange(account.exchange.pk).default_blockchain
    token_obj, token_created = Token.objects.get_or_create(
        name=get_token_full_name(account, token), symbol=token, blockchain=blockchain
    )
    if quantity:
        AccountTokens(account=account, token=token_obj, quantity=quantity).save()
    return token_obj
