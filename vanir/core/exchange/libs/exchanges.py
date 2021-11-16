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
    """Extended Exchange Registry class creator"""

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
    """Base Basic Exchange class"""

    @abstractmethod
    def __init__(self, account):
        self.account = account
        self.api_key = account.api_key
        self.api_secret = account.secret
        self.tld = account.tld
        self.testnet = account.testnet

    @abstractmethod
    def test(self) -> bool:
        """
        Add test method to see if the exchange is properly
        configured
        :return: True if all okay, false otherwise
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def get_balance(self) -> pd.DataFrame:
        """
        Method to get balance of the account in Panda Data Frame
        :return: Data Frame with data
        :rtype: pandas.DataFrame
        """
        raise NotImplementedError

    @abstractmethod
    def all_assets_prices(self) -> dict:
        """
        Return price of all assets in the exchange
        :return: Current price of all assets in the exchange
        :rtype: dict
        """
        pass

    def get_token_base_price(self, token1: str, token2: str) -> float:
        """
        Returns the price for specific ticker (pair)
        :param token1: Token one
        :param token2: Token two (pair)
        :return: Price of the token
        :rtype: float
        """
        raise NotImplementedError

    @abstractmethod
    def order_process(self, *args, **kwargs):
        """
        Process order on the exchange
        :param args: Order args
        :param kwargs: Order kwargs
        """
        raise NotImplementedError

    @abstractmethod
    def get_token_full_name(self, symbol: str) -> str:
        """
        Get token symbol and returns the name
        :param symbol: Symbol to query
        :return: Token name
        :rtype: str
        """
        raise NotImplementedError

    @abstractmethod
    def order_validation(self, *args, **kwargs):
        """
        Validates the order before placing it
        :param args: Order validation args
        :param kwargs: Order validation kwargs
        """
        pass

    @abstractmethod
    def order_correction(self, *args, **kwargs):
        """
        Corrects the order if it contains problems
        and possible
        :param args: Order validation args
        :param kwargs: Order validation kwargs
        :return: Sanitise order
        """
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

    def get_balance_pd(self) -> pd.DataFrame:
        account = self.get_account()
        balance = [
            asset
            for asset in account["balances"]
            if not (
                float(asset["free"]) <= 0.1 / 10e9
                and float(asset["locked"]) <= 0.1 / 10e9
            )
        ]
        try:
            df = pd.DataFrame(balance).sort_values(by=["free"], ascending=False)
        except KeyError:
            df = pd.DataFrame(balance)
        return df

    def get_balance_html(self):
        df = self.get_balance_pd()
        response = change_table_style(df.to_html(classes="table table-striped"))
        response = change_table_align(response)
        return response

    def get_balance(self) -> dict:
        df = self.get_balance_pd()
        balance_dict = {}
        if df is not None:
            try:
                for index, row in df.iterrows():
                    # Catch APENFT vs NFT problem with Binance
                    if row["asset"] == "NFT":
                        symbol = "APENFT"
                    else:
                        symbol = row["asset"]
                    balance_dict[symbol] = float(row["free"]) + float(row["locked"])
            except AttributeError:
                pass
        return balance_dict

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
        """
        Get margin all assets from API
        :return: Dictionary with symbol and asset name
        :rtype: dict
        """
        all_margin_assets = {}
        margin_assets = self.con.get_margin_all_assets()
        for asset in margin_assets:
            all_margin_assets.update({asset["assetName"]: asset["assetFullName"]})
        return all_margin_assets

    def get_token_full_name(self, symbol: str) -> str:
        """
        Try to get the name of the symbol by querying coins list
        :param symbol: Token to check the name
        :return: Name if found, symbol otherwise
        :rtype: str
        """
        try:
            name = self.all_margin_assets[symbol]
        except KeyError:
            return symbol
        return name

    def get_token_base_price(self, token1: str, token2: str):
        """
        Get the price of a single token
        :param token1: String symbol first token
        :param token2: String symbol second token
        :return: None or price
        :rtype: None or float
        """
        if token2 == "USD":
            token2 = "USDT"
        try:
            price = self.get_avg_price(symbol=f"{token1}{token2}")["price"]
        except BinanceAPIException as binanceexception:
            if binanceexception.code == -1121:
                logger.error(f"Pair {token1}{token2} not supported")
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
