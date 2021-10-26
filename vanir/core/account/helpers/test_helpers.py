from vanir.core.account.models import Account


def aux_create_basic_account(
    name,
    exchange,
    token_pair,
    api_key="account1_1234",
    secret="1234secret",
    default=True,
):
    account_create = Account.objects.create(
        name=name,
        exchange=exchange,
        api_key=api_key,
        secret=secret,
        token_pair=token_pair,
        default=default,
    )
    return account_create
