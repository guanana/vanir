from abc import ABC, abstractmethod

from vanir.account.models import Account


class BasicExchange(ABC):
    @abstractmethod
    def __init__(self, account: Account):
        self.api_key = account.api_key
        self.api_secret = account.secret
        self.tld = account.tld

    @abstractmethod
    def con(self):
        raise NotImplementedError

    @abstractmethod
    def test(self):
        raise NotImplementedError

    @abstractmethod
    def get_balance(self):
        raise NotImplementedError