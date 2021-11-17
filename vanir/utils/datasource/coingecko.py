from pycoingecko import CoinGeckoAPI

from vanir.core.exchange.libs.exchanges import BasicExchange
from vanir.core.token.models import Token
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
        all_symbols = list(Token.objects.all().values_list("symbol", flat=True))
        cg_coins_list = self.get_coins_list()
        coins_dict_by_symbol = {item['symbol']: item['id'] for item in cg_coins_list}
        coins_dict_by_id = {item['id']: item['symbol'] for item in cg_coins_list}
        ids = [coins_dict_by_symbol[symbol.lower()] for symbol in all_symbols
               if symbol.lower() in coins_dict_by_symbol.keys()]
        prices = self.get_price(ids=ids, vs_currencies=vs_currency)
        for asset, value in prices.items():
            try:
                temp_prices[f'{coins_dict_by_id[asset].upper()}{vs_currency.upper()}'] = float(value[vs_currency])
            except KeyError:
                temp_prices[f'{coins_dict_by_id[asset].upper()}{vs_currency.upper()}'] = float(0)

        return temp_prices

    def get_token_base_price(self, symbol1, symbol2="usd"):
        """
        Gets the price that is going to be inserted in the history, by default USD
        Alias of get_fiat_price
        :param symbol1: Symbol of the token
        :param symbol2: Symbol of the pair, by default USD
        :return: price of symbol
        :rtype: float
        """
        return self.get_fiat_price(symbol1, symbol2)

    def get_fiat_price(self, symbol1, fiat="usd"):
        """
        Get fiat price of certain symbol
        :param symbol1: symbol to check against fiat
        :param fiat: fiat symbol
        :return: price of symbol
        :rtype: float
        """
        token1 = self.get_token_full_name(symbol1)
        if fiat.upper() in dollar_pairs:
            price = self.get_price(ids=token1, vs_currencies="USD")
            return float(price[token1]["usd"])
        elif fiat.lower() in self.get_supported_vs_currencies():
            price = self.get_price(ids=token1, vs_currencies=fiat.lower())
            return float(price[token1][fiat.lower()])
        else:
            raise PairNotSupportedError()

    def get_token_full_name(self, symbol: str) -> str:
        """
        Try to get the name of the symbol by querying coins list
        :param symbol: Token to check the name
        :return: Name if found, symbol otherwise
        :rtype: str
        """
        all_tokens = self.get_coins_list()
        name = [token["name"] for token in all_tokens if symbol == token["symbol"]]
        try:
            return name[0].lower()
        except (TypeError, IndexError):
            return symbol
