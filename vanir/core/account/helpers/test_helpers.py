from vanir.core.account.models import Account


def aux_create_basic_account(
    name: str,
    exchange,
    token_pair,
    api_key: str = "account1_1234",
    secret: str = "1234secret",
    default: bool = True,
) -> Account:
    """
    Aux function to create accounts for tests
    :param name: Account name
    :type name: str
    :param exchange: Exchange linked to the account
    :type exchange: str
    :param token_pair: Token object to be used as pair
    :type token_pair: Token
    :param api_key: Api key, useful only for supported exchanges
    :type api_key: str
    :param secret: Secret key, useful only for supported exchanges
    :type secret: str
    :param default: Default account in the system
    :type default: bool
    :return: Account object
    :rtype: Account
    """
    account_create = Account.objects.create(
        name=name,
        exchange=exchange,
        api_key=api_key,
        secret=secret,
        token_pair=token_pair,
        default=default,
    )
    return account_create
