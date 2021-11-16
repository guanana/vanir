from vanir.core.token.helpers.import_utils import bulk_update, import_token_account, token_import
from vanir.core.token.models import Token


def update_balance(account, update_price: bool = True):
    """
    Fetch, primarily from Binance, the account balance
    and parse the values to create/update tokens
    :param account: Account object to get the balance
    :type account: Account
    :param update_price: Specify if just want to get
    balance or price as well
    :type update_price: bool
    :return: List of symbols imported
    :rtype: list
    """
    balance_dict = account.exchange_obj.get_balance()
    response = []
    if balance_dict is not None:
        try:
            for symbol, value in balance_dict.items():
                try:
                    token = Token.objects.get(symbol=symbol)
                except Token.DoesNotExist:
                    token = token_import(account=account, token_symbol=symbol)
                import_token_account(
                    account=account,
                    token_obj=token,
                    quantity=value,
                )
                response.append(symbol)
        except AttributeError:
            pass
    if update_price:
        bulk_update(account)
    return response
