from pycoingecko import CoinGeckoAPI

from vanir.core.exchange.libs.exchanges import BasicExchange
from vanir.utils.exceptions import PairNotSupportedError


class CoinGeckoVanir(CoinGeckoAPI, BasicExchange):
    def test(self):
        response = self.ping()
        try:
            if response["gecko_says"]:
                return True
        except AttributeError:
            return False

    def get_balance(self):
        return None

    @property
    def all_assets_prices(self, vs_currency="usd"):
        temp_prices = {}
        for asset in self.get_coins_markets(vs_currency=vs_currency):
            temp_prices[f'{asset["symbol"].upper()}{vs_currency.upper()}'] = float(
                asset["current_price"]
            )
        return temp_prices

    def get_name_by_symbol(self, symbol):
        all_tokens = self.get_coins_list()
        name = [token["name"] for token in all_tokens if symbol == token["symbol"]]
        try:
            return name[0].lower()
        except TypeError:
            return "Unknown"

    def get_fiat_price(self, symbol1, fiat="usd"):
        token1 = self.get_name_by_symbol(symbol1)
        dollar_pairs = ("BUSD", "USDT", "USDC", "DAI", "UST", "TUSD", "USDP")
        if fiat.upper() in dollar_pairs:
            price = self.get_price(ids=token1, vs_currencies="USD")
            return float(price[token1]["usd"])
        elif fiat.lower() in self.get_supported_vs_currencies():
            price = self.get_price(ids=token1, vs_currencies=fiat.lower())
            return float(price[token1][fiat.lower()])
        else:
            raise PairNotSupportedError()