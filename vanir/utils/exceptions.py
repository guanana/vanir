from vanir.utils import constants_exceptions


#
# Exchange Exceptions
#
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


class ExchangeInvalidSymbolError(ExchangeError):
    """
    Invalid symbol
    """

    def __init__(
        self,
        message: str = constants_exceptions.EXCHANGEINVALIDSYMBOLERROR,
        account=None,
    ):
        self.message = message
        super().__init__(self.message, account)


class ExchangeInvalidQuantityError(ExchangeError):
    """
    Invalid Quantity
    """

    def __init__(
        self,
        message: str = constants_exceptions.EXCHANGEINVALIDQUANTITYERROR,
        account=None,
    ):
        self.message = message
        super().__init__(self.message, account)


class ExchangeExtendedFunctionalityError(ExchangeError):
    """
    Extended Exchange not found
    """

    def __init__(
        self,
        message: str = constants_exceptions.EXCHANGEEXTENDEDFUNCTIONALITYERROR,
        account=None,
    ):
        self.message = message
        super().__init__(self.message, account)


#
# Account Exceptions
#
class AccountError(Exception):
    """
    Base Exception Class for Exchange problems
    """

    def __init__(self, message: str = "AccountError", account=None):
        self.message = message
        super().__init__(self.message)
        self.account = account

    def __str__(self):
        if self.account:
            return f"{self.account}: ***{self.account.name} -> {self.message}"
        else:
            return self.message


class AccountRequiredError(ExchangeError):
    """
    At least one account is required
    """

    def __init__(
        self,
        message: str = constants_exceptions.ACCOUNTREQUIREDERROR,
        account=None,
    ):
        self.message = message
        super().__init__(self.message, account)
