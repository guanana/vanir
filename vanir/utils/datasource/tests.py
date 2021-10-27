from unittest.mock import patch

from django.test import TestCase

from vanir.core.account.helpers.test_helpers import aux_create_basic_account
from vanir.core.exchange.models import Exchange
from vanir.core.token.models import Token

ping_dict = {"gecko_says": "(V3) To the Moon!"}
all_coins_list = [
    {"id": "binance", "symbol": "BNB", "name": "Binance Coin"},
    {"id": "ethereum", "symbol": "ETH", "name": "Ethereum"},
]


class TestAccountHelpers(TestCase):
    def setUp(self):
        self.token = Token.objects.create(name="Test Helper", symbol="TSTHELP")
        self.manual_exchange = Exchange.objects.create(
            name="exchange_test", native_token=self.token
        )
        self.manual_account = aux_create_basic_account(
            name="account1", exchange=self.manual_exchange, token_pair=self.token
        )

    @patch("pycoingecko.api.CoinGeckoAPI.ping", return_value=ping_dict)
    def test_coingecko_test_okay(self, mock_pycoingecko_ping):
        test = self.manual_account.exchange_obj.test()
        self.assertEqual(test, True)
        self.assertEqual(mock_pycoingecko_ping.called, True)

    @patch("pycoingecko.api.CoinGeckoAPI.ping", return_value={})
    def test_coingecko_test_no_okay(self, mock_pycoingecko_ping):
        test = self.manual_account.exchange_obj.test()
        self.assertEqual(test, False)
        self.assertEqual(mock_pycoingecko_ping.called, True)

    @patch("pycoingecko.api.CoinGeckoAPI.get_coins_list", return_value=all_coins_list)
    def test_coingecko_get_name_by_symbol(self, mock_pycoingecko_all_coins_list):
        bnb_name = self.manual_account.exchange_obj.get_name_by_symbol("BNB")
        self.assertEqual(bnb_name, "binance coin")
        self.assertEqual(mock_pycoingecko_all_coins_list.called, True)

    @patch("pycoingecko.api.CoinGeckoAPI.get_coins_list", return_value=all_coins_list)
    def test_coingecko_get_name_by_symbol_not_found(
        self, mock_pycoingecko_all_coins_list
    ):
        eos_name = self.manual_account.exchange_obj.get_name_by_symbol("EOS")
        self.assertEqual(eos_name, "Unknown")
        self.assertEqual(mock_pycoingecko_all_coins_list.called, True)

    @patch("vanir.utils.datasource.coingecko.CoinGeckoVanir.get_coins_markets")
    def test_account_get_balance_manual(self, mock_coingecko_price):
        df = self.manual_account.exchange_obj.get_balance()
        self.assertIsNone(df)
        self.assertEqual(mock_coingecko_price.called, False)
