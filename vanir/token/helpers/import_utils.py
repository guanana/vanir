from vanir.account.models import Account
from vanir.account.models_relation import AccountTokens
from vanir.blockchain.models import Blockchain
from vanir.token.models import Token


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
