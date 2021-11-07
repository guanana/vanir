from pycoingecko import CoinGeckoAPI

from vanir.core.exchange.libs.exchanges import BasicExchange
from vanir.utils.exceptions import PairNotSupportedError
from vanir.utils.token_constants import dollar_pairs


class CoinGeckoVanir(CoinGeckoAPI, BasicExchange):
    """ CoinGecko Model"""

    def test(self):
        """
        Test connection to coingecko
        :return: True if success, false otherwise
        :rtype: bool
        """
        response = self.ping()
        try:
            if response["gecko_says"]:
                return True
        except (AttributeError, KeyError):
            return False

    def get_balance(self):
        """
        Not necessary for Coingecko (no balance since it's not Exchange as such)
        :return: None
        :rtype: None
        """
        return None

    @property
    def all_assets_prices(self, vs_currency="usd"):
        """
        Get all assets in coingecko, by default checks for usd pair,
        standard function of exchange base
        :param vs_currency: Pair to check the price against
        :return: dictionary with the price
        :rtype: dict
        """
        temp_prices = {}
        for asset in self.get_coins_markets(vs_currency=vs_currency):
            temp_prices[f'{asset["symbol"].upper()}{vs_currency.upper()}'] = float(
                asset["current_price"]
            )
            if vs_currency == "usd":
                # Add USDT as well by default
                temp_prices[f'{asset["symbol"].upper()}{vs_currency.upper()}T'] = float(
                    asset["current_price"]
                )
        return temp_prices

    def get_name_by_symbol(self, symbol):
        """
        Try to get the name of the symbol by querying coins list
        :param symbol: Symbol to check the name
        :return: Name if found, unknown otherwise
        :rtype: str
        """
        all_tokens = self.get_coins_list()
        name = [token["name"] for token in all_tokens if symbol == token["symbol"]]
        try:
            return name[0].lower()
        except (TypeError, IndexError):
            return "Unknown"

    def get_fiat_price(self, symbol1, fiat="usd"):
        """
        Get fiat price of certain symbol
        :param symbol1: symbol to check against fiat
        :param fiat: fiat symbol
        :return: price of symbol
        :rtype: float
        """
        token1 = self.get_name_by_symbol(symbol1)
        if fiat.upper() in dollar_pairs:
            price = self.get_price(ids=token1, vs_currencies="USD")
            return float(price[token1]["usd"])
        elif fiat.lower() in self.get_supported_vs_currencies():
            price = self.get_price(ids=token1, vs_currencies=fiat.lower())
            return float(price[token1][fiat.lower()])
        else:
            raise PairNotSupportedError()
