import json
from unittest.mock import PropertyMock, patch

from django.test import TestCase
from pycoingecko import CoinGeckoAPI

from vanir.core.account.helpers.test_helpers import aux_create_basic_account
from vanir.core.exchange.models import Exchange
from vanir.core.token.models import Token
from vanir.utils.datasource.fiat_convertor import FiatConvertorVanir

ping_dict = {"gecko_says": "(V3) To the Moon!"}
all_coins_list = [
    {"id": "binance", "symbol": "BNB", "name": "Binance Coin"},
    {"id": "ethereum", "symbol": "ETH", "name": "Ethereum"},
]
price_dict = {"ethereum": {"usd": 30}}
supported_fiat_list = [
    "btc",
    "eth",
    "ltc",
    "bch",
    "bnb",
    "eos",
    "xrp",
    "xlm",
    "link",
    "dot",
    "yfi",
    "usd",
    "aed",
    "ars",
    "aud",
    "bdt",
    "bhd",
    "bmd",
    "brl",
    "cad",
    "chf",
    "clp",
    "cny",
    "czk",
    "dkk",
    "eur",
    "gbp",
    "hkd",
    "huf",
    "idr",
    "ils",
    "inr",
    "jpy",
    "krw",
    "kwd",
    "lkr",
    "mmk",
    "mxn",
    "myr",
    "ngn",
    "nok",
    "nzd",
    "php",
    "pkr",
    "pln",
    "rub",
    "sar",
    "sek",
    "sgd",
    "thb",
    "try",
    "twd",
    "uah",
    "vef",
    "vnd",
    "zar",
    "xdr",
    "xag",
    "xau",
    "bits",
    "sats",
]


class TestAccountHelpers(TestCase):
    @patch("vanir.core.account.helpers.balance.update_balance")
    def setUp(self, mock_update_balance):
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
        bnb_name = self.manual_account.exchange_obj.get_token_full_name("BNB")
        self.assertEqual(bnb_name, "binance coin")
        self.assertEqual(mock_pycoingecko_all_coins_list.called, True)

    @patch("pycoingecko.api.CoinGeckoAPI.get_coins_list", return_value=all_coins_list)
    def test_coingecko_get_name_by_symbol_not_found(
        self, mock_pycoingecko_all_coins_list
    ):
        eos_name = self.manual_account.exchange_obj.get_token_full_name("EOS")
        self.assertEqual(eos_name, "EOS")
        self.assertEqual(mock_pycoingecko_all_coins_list.called, True)

    @patch("vanir.utils.datasource.coingecko.CoinGeckoVanir.get_coins_list")
    def test_account_get_balance_manual(self, mock_coingecko_price):
        balance = self.manual_account.exchange_obj.get_balance()
        self.assertIsNone(balance)
        self.assertEqual(mock_coingecko_price.called, False)

    @patch.object(
        CoinGeckoAPI, "get_coins_list", autospec=True, return_value=all_coins_list
    )
    @patch.object(CoinGeckoAPI, "get_price", autospec=True, return_value=price_dict)
    @patch.object(
        CoinGeckoAPI,
        "get_supported_vs_currencies",
        autospec=True,
        return_value=supported_fiat_list,
    )
    def test_get_fiat_price_usd(
        self, mock_supported_fiat_list, mock_pycoingecko_all_coins_list, mock_get_price
    ):
        price = self.manual_account.exchange_obj.get_fiat_price("ETH")
        self.assertEqual(price, 30)
        self.assertEqual(mock_pycoingecko_all_coins_list.call_count, 1)
        self.assertEqual(mock_get_price.call_count, 1)
        self.assertEqual(mock_supported_fiat_list.called, False)


exchange_rate_dict = {"result": "success",
                      "provider": "https://www.exchangerate-api.com",
                      "documentation": "https://www.exchangerate-api.com/docs/free",
                      "terms_of_use": "https://www.exchangerate-api.com/terms",
                      "time_last_update_unix": 1636329751,
                      "time_last_update_utc": "Mon, 08 Nov 2021 00:02:31 +0000",
                      'time_next_update_unix': 1636416461,
                      'time_next_update_utc': 'Tue, 09 Nov 2021 00:07:41 +0000',
                      'time_eol_unix': 0,
                      'base_code': 'USD',
                      'rates': {'USD': 1,
                                'AUD': 1.35,
                                'BMD': 1,
                                'BSD': 1,
                                'BTN': 74.46,
                                'EUR': 0.865,
                                'GBP': 0.741,
                                'NZD': 1.41,
                                'RSD': 101.98,
                                'RUB': 71.35
                                }
                      }


class TestFiatConvertor(TestCase):
    def test_api_get(self):
        with patch('requests.get') as mock_request:
            url = "https://open.er-api.com/v6/latest/USD" # noqa F841
            fiatconverter = FiatConvertorVanir()
            type(mock_request.return_value).content = PropertyMock(return_value=json.dumps(exchange_rate_dict))
            rates = fiatconverter.rates()
            self.assertEqual(rates, exchange_rate_dict["rates"])
            self.assertEqual(mock_request.called, True)

    def test_convert_fiat(self):
        with patch('requests.get') as mock_request:
            url = "https://open.er-api.com/v6/latest/USD" # noqa F841
            fiatconverter = FiatConvertorVanir()
            type(mock_request.return_value).content = PropertyMock(return_value=json.dumps(exchange_rate_dict))
            usd_to_eur = fiatconverter.convert_from("EUR", 1)
            self.assertEqual(usd_to_eur, 0.865)
            self.assertEqual(mock_request.called, True)
