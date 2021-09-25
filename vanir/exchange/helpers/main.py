from abc import abstractmethod


class ExtendedExchangeRegistry(type):
    registered = {}

    def __new__(mcs, name, bases, attrs):
        # create the new type
        newclass = type.__new__(mcs, name, bases, attrs)
        mcs.registered[name] = newclass
        return type.__new__(mcs, name, bases, attrs)

    @classmethod
    def get_class_by_name(mcs, name):
        if name in mcs.registered.keys():
            return mcs.registered[name]
        else:
            return mcs.registered[f"Vanir{name}"]

    @classmethod
    def all_supported(mcs):
        return mcs.registered.keys()


class BasicExchange:
    @abstractmethod
    def __init__(self, account):
        self.api_key = account.api_key
        self.api_secret = account.secret
        self.tld = account.tld
        self.testnet = account.testnet

    @abstractmethod
    def default_blockchain(self):
        raise NotImplementedError

    @abstractmethod
    def con(self):
        raise NotImplementedError

    @abstractmethod
    def test(self):
        raise NotImplementedError

    @abstractmethod
    def get_balance(self):
        raise NotImplementedError

    @abstractmethod
    def all_assets_prices(self) -> dict:
        pass


class ExtendedExchange(BasicExchange, metaclass=ExtendedExchangeRegistry):
    pass
