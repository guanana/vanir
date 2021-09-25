import pandas as pd
from binance import Client
from binance.exceptions import BinanceAPIException
from django.core.exceptions import ValidationError

from vanir.blockchain.models import Blockchain
from vanir.exchange.helpers.main import ExtendedExchange, ExtendedExchangeRegistry
from vanir.exchange.models import Exchange
from vanir.utils.table_helpers import change_table_align, change_table_style


class VanirBinance(ExtendedExchange, Client, metaclass=ExtendedExchangeRegistry):
    def __init__(self, account):
        self.all_margin_assets = {}
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
        blockchain = Exchange.objects.get(name__startswith="Binance").default_blockchain
        if not blockchain:
            try:
                return Blockchain.objects.get(name__startswith="Binance")
            except Blockchain.DoesNotExist:
                raise ValidationError(
                    "You need to define a default blockchain on the exchange"
                )
        else:
            return blockchain

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

    def get_balance(self) -> pd.DataFrame:
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

    def get_all_assets(self):
        if not self.all_margin_assets:
            margin_assets = self.con.get_margin_all_assets()
            for asset in margin_assets:
                self.all_margin_assets.update(
                    {asset["assetName"]: asset["assetFullName"]}
                )
        return self.all_margin_assets

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
