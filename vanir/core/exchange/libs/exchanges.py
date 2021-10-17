import logging
from abc import abstractmethod

import pandas as pd
from binance import Client
from binance.exceptions import BinanceAPIException
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from vanir.core.blockchain.models import Blockchain
from vanir.core.exchange.libs.orders import Orders
from vanir.utils.exceptions import (
    ExchangeInvalidQuantityError,
    ExchangeInvalidSymbolError,
    ExchangeNotEnoughPrivilegesError,
)
from vanir.utils.table_helpers import change_table_align, change_table_style

logger = logging.getLogger(__name__)


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
        self.account = account
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

    @abstractmethod
    def order_process(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def order_validation(self, *args, **kwargs):
        pass

    @abstractmethod
    def order_correction(self, *args, **kwargs):
        pass


class ExtendedExchange(BasicExchange, metaclass=ExtendedExchangeRegistry):
    pass


#
# VANIR BINANCE
#
class VanirBinance(ExtendedExchange, Client, metaclass=ExtendedExchangeRegistry):
    def __init__(self, account):
        self.name = "VanirBinance"
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
        return Blockchain.objects.get(name__contains="Binance")

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
    def pairs_info(self):
        full_info = self.get_exchange_info()
        pairs_info = {}
        # First iteration to create all the keys
        for symbol_raw in full_info["symbols"]:
            if symbol_raw["status"] == "TRADING":
                try:
                    pairs_info[symbol_raw["baseAsset"]].append(symbol_raw["quoteAsset"])
                except KeyError:
                    pairs_info[symbol_raw["baseAsset"]] = []
        return pairs_info

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
                logger.error(f"Pair {pair} not supported")
            return

        try:
            return float(price)
        except ValueError:
            return

    @property
    def all_assets_prices(self):
        temp_prices = {}
        for asset in self.get_all_tickers():
            temp_prices[asset["symbol"]] = float(asset["price"])
        return temp_prices

    def order_test(self, **kwargs):
        try:
            order_test = self.con.create_test_order(**kwargs)
            return order_test
        except BinanceAPIException as binanceexception:
            if binanceexception.code == -2015:
                raise ExchangeNotEnoughPrivilegesError(account=self.account)
            elif binanceexception.code == -1121:
                raise ExchangeInvalidSymbolError(account=self.account)
            elif binanceexception.code == -1013:
                if kwargs.get("quantity") <= 0:
                    raise ValidationError("Value cannot be 0 for an order")
                else:
                    raise ExchangeInvalidQuantityError(account=self.account)
            else:
                return binanceexception

    def order_validation(self, **kwargs):
        order_obj = Orders(**kwargs)
        try:
            self.order_test(**order_obj.binance_args)
            order_obj.validated = True
        except ExchangeInvalidQuantityError:
            order_obj.validated = self.order_quantity_correction(order_obj)
        return order_obj, order_obj.validated

    def order_quantity_correction(self, order_obj):
        symbol_info = self.con.get_symbol_info(order_obj.symbol)
        mandatory_precision = symbol_info["baseAssetPrecision"]
        # Fix precision
        corrected = order_obj.correct_precision(mandatory_precision)
        return corrected
