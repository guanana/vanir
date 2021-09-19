import pandas as pd
from binance import Client
from binance.exceptions import BinanceAPIException

from vanir.account.models import Account
from vanir.exchange.helpers.main import BasicExchange
from vanir.utils.helpers import change_table_align, change_table_style


class VanirBinance(BasicExchange):
    def __init__(self, account: Account):
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

    def get_balance(self):
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
        response = change_table_style(df.to_html(classes="table table-striped"))
        response = change_table_align(response)
        return response
