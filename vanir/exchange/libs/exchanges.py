from abc import abstractmethod

import pandas as pd
from binance import Client
from binance.exceptions import BinanceAPIException
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from vanir.blockchain.models import Blockchain
from vanir.exchange.models import Exchange
from vanir.utils.table_helpers import change_table_align, change_table_style


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
        temp_list = mcs.registered.copy()
        temp_list.pop("ExtendedExchange")
        list_iter = temp_list.copy()
        for key in list_iter.keys():
            temp_list[key.replace("Vanir", "")] = temp_list.pop(key)
        return ",".join(temp_list.keys())


class BasicExchange:
    @abstractmethod
    def __init__(self, account):
        self.api_key = account.api_key
        self.api_secret = account.secret
        self.tld = account.tld
        self.testnet = account.testnet

    @abstractmethod
    def default_blockchain(self) -> Blockchain:
        raise NotImplementedError

    @abstractmethod
    def con(self):
        raise NotImplementedError

    @abstractmethod
    def test(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_balance(self) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def all_assets_prices(self) -> dict:
        pass


class ExtendedExchange(BasicExchange, metaclass=ExtendedExchangeRegistry):
    pass


#
# VANIR BINANCE
#
class VanirBinance(ExtendedExchange, Client, metaclass=ExtendedExchangeRegistry):
    def __init__(self, account):
        self.testnet = False
        super(ExtendedExchange, self).__init__(account)
        super(Client, self).__init__(
            api_key=self.api_key,
            api_secret=self.api_secret,
            tld=self.tld,
            testnet=self.testnet,
        )

    @property
    def default_blockchain(self):
        try:
            exchange_model = Exchange.objects.get(name__startswith="Binance")
        except Blockchain.DoesNotExist:
            raise ValidationError(
                "You need to define a default blockchain on the exchange"
            )
        return exchange_model.default_blockchain

    @property
    def con(self):
        return Client(
            api_key=self.api_key,
            api_secret=self.api_secret,
            tld=self.tld,
            testnet=self.testnet,
        )

    def test(self):
        try:
            self.get_account()
            return True
        except BinanceAPIException:
            return False

    def get_balance(self):
        account = self.get_account()
        balance = [
            asset
            for asset in account["balances"]
            if not (
                float(asset["free"]) <= 0.1 / 10e9
                and float(asset["locked"]) <= 0.1 / 10e9
            )
        ]
        df = pd.DataFrame(balance).sort_values(by=["free"], ascending=False)
        return df

    def get_balance_html(self):
        df = self.get_balance()
        response = change_table_style(df.to_html(classes="table table-striped"))
        response = change_table_align(response)
        return response

    @cached_property
    def all_margin_assets(self):
        all_margin_assets = {}
        margin_assets = self.con.get_margin_all_assets()
        for asset in margin_assets:
            all_margin_assets.update({asset["assetName"]: asset["assetFullName"]})
        return all_margin_assets

    def get_token_price(self, pair):
        try:
            price = self.get_avg_price(symbol=f"{pair}")["price"]
        except BinanceAPIException as binanceexception:
            if binanceexception.code == -1121:
                raise ValueError(f"Pair {pair} not supported")

        try:
            return float(price)
        except ValueError:
            return None

    @property
    def all_assets_prices(self):
        temp_prices = {}
        for asset in self.get_all_tickers():
            temp_prices[asset["symbol"]] = float(asset["price"])
        return temp_prices
