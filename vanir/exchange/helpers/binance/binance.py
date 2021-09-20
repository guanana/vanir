import pandas as pd
from binance import Client
from binance.exceptions import BinanceAPIException

from vanir.account.models import Account
from vanir.exchange.helpers.main import BasicExchange
from vanir.exchange.models import Exchange
from vanir.utils.helpers import change_table_align, change_table_style


class VanirBinance(BasicExchange):
    def __init__(self, account: Account):
        self.all_margin_assets = {}
        self.default_blockchain = Exchange.objects.get(
            name__startswith="Binance"
        ).default_blockchain
        super().__init__(account)

    @property
    def con(self):
        return Client(api_key=self.api_key, api_secret=self.api_secret, tld=self.tld)

    def test(self):
        try:
            self.con.get_account()
            return True
        except BinanceAPIException:
            return False

    def get_balance(self) -> pd.DataFrame:
        account = self.con.get_account()
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
