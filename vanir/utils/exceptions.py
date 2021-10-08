from vanir.utils import constants_exceptions


class ExchangeError(Exception):
    """
    Base Exception Class for Exchange problems
    """

    def __init__(self, message: str = "ExchangeError", account=None):
        self.message = message
        super().__init__(self.message)
        self.account = account

    def __str__(self):
        if self.account:
            return f"{self.account} with API KEY: ***{self.account.api_key[-3:]} -> {self.message}"
        else:
            return self.message


class ExchangeConnectionError(ExchangeError):
    """
    Problem to connect to API
    """

    def __init__(
        self, message: str = constants_exceptions.EXCHANGECONNECTIONERROR, account=None
    ):
        self.message = message
        super().__init__(self.message, account)


class ExchangeNotEnoughPrivilegesError(ExchangeError):
    """
    Problem permissions
    """

    def __init__(
        self, message: str = constants_exceptions.EXCHANGEPRIVILEGESERROR, account=None
    ):
        self.message = message
        super().__init__(self.message, account)
