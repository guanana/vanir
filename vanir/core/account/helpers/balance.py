from vanir.core.token.helpers.import_utils import (
    bulk_update,
    import_token_account,
    token_import,
)
from vanir.core.token.models import Token


def update_balance(account, update_price=True):
    df = account.exchange_obj.get_balance()
    response = []
    for index, row in df.iterrows():
        try:
            token = Token.objects.get(symbol=row["asset"])
        except Token.DoesNotExist:
            token = token_import(account=account, token_symbol=row["asset"])
        import_token_account(
            account=account,
            token_obj=token,
            quantity=float(row["free"]) + float(row["locked"]),
        )
        response.append(row["asset"])
    if update_price:
        bulk_update(account)
    return response
