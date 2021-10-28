from unittest.mock import patch

from binance import Client
from django.test import TestCase

from vanir.core.account.helpers.balance import update_balance
from vanir.core.account.helpers.test_helpers import aux_create_basic_account
from vanir.core.account.models import Account
from vanir.core.exchange.models import Exchange
from vanir.core.token.models import Token

account_mock_dict = {
    "makerCommission": 10,
    "takerCommission": 10,
    "buyerCommission": 0,
    "sellerCommission": 0,
    "canTrade": True,
    "canWithdraw": True,
    "canDeposit": True,
    "updateTime": 1635129047375,
    "accountType": "SPOT",
    "balances": [
        {"asset": "BTC", "free": "0.00014051", "locked": "0.00000000"},
        {"asset": "LTC", "free": "0.01530277", "locked": "0.07693000"},
        {"asset": "ETH", "free": "0.00401792", "locked": "0.00000000"},
        {"asset": "NEO", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "BNB", "free": "0.09387603", "locked": "0.00000000"},
        {"asset": "QTUM", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "EOS", "free": "10.64085300", "locked": "10.00000000"},
        {"asset": "SNT", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "BCC", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "USDT", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "HSR", "free": "0.00000000", "locked": "0.00000000"},
    ],
    "permissions": ["SPOT"],
}
account_mock_dict_empty_balance = {
    "makerCommission": 10,
    "takerCommission": 10,
    "buyerCommission": 0,
    "sellerCommission": 0,
    "canTrade": True,
    "canWithdraw": True,
    "canDeposit": True,
    "updateTime": 1635129047375,
    "accountType": "SPOT",
    "balances": [
        {"asset": "BTC", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "LTC", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "ETH", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "NEO", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "BNB", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "QTUM", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "EOS", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "SNT", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "BCC", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "USDT", "free": "0.00000000", "locked": "0.00000000"},
        {"asset": "HSR", "free": "0.00000000", "locked": "0.00000000"},
    ],
    "permissions": ["SPOT"],
}
get_margin_all_assets_mock_dict = [
    {
        "assetFullName": "USD coin",
        "assetName": "USDC",
        "isBorrowable": True,
        "isMortgageable": True,
        "userMinBorrow": "0.00000000",
        "userMinRepay": "0.00000000",
    },
    {
        "assetFullName": "BNB-coin",
        "assetName": "BNB",
        "isBorrowable": True,
        "isMortgageable": True,
        "userMinBorrow": "1.00000000",
        "userMinRepay": "0.00000000",
    },
    {
        "assetFullName": "Etherum",
        "assetName": "ETH",
        "isBorrowable": True,
        "isMortgageable": True,
        "userMinBorrow": "1.00000000",
        "userMinRepay": "0.00000000",
    },
]

get_all_tickers_mock = [
    {"symbol": "ETHUSD", "price": "1.06720800"},
    {"symbol": "ETHUSDT", "price": "1.06720800"},
    {"symbol": "LTCBTC", "price": "0.00306600"},
    {"symbol": "BNBBTC", "price": "0.00768100"},
    {"symbol": "EOSETH", "price": "0.00105500"},
    {"symbol": "GASBTC", "price": "0.00014040"},
    {"symbol": "BNBETH", "price": "0.11440000"},
    {"symbol": "BTCUSDT", "price": "58410.13000000"},
    {"symbol": "ICNETH", "price": "0.00166300"},
    {"symbol": "MCOBTC", "price": "0.00021140"},
    {"symbol": "WTCBTC", "price": "0.00001578"},
]


def side_effect_get_token_full_name(account, token_symbol):
    return token_symbol


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
        self.bnb = Token.objects.create(symbol="BNB", name="Binance Coin")
        self.binance = Exchange.objects.create(name="Binance", native_token=self.bnb)

    @patch("vanir.utils.datasource.coingecko.CoinGeckoVanir.get_coins_markets")
    def test_account_update_balance_no_price_manual(self, mock_coingecko_price):
        response = update_balance(self.manual_account, update_price=False)
        self.assertEqual(response, [])
        self.assertEqual(mock_coingecko_price.call_count, 0)

    @patch("vanir.utils.datasource.coingecko.CoinGeckoVanir.get_coins_markets")
    def test_account_update_balance_price_manual(self, mock_coingecko_price):
        response = update_balance(self.manual_account, update_price=True)
        self.assertEqual(response, [])
        self.assertEqual(mock_coingecko_price.call_count, 1)

    @patch(
        "binance.client.Client.get_account",
        return_value=account_mock_dict_empty_balance,
    )  # noqa
    @patch.object(Client, "get_all_tickers", autospec=True)
    def test_account_update_balance_empty_binance_no_price(
        self, mock_get_all_tickers, mock_get_account  # noqa
    ):
        with patch("vanir.core.account.helpers.balance.update_balance"):
            binance_account = Account.objects.create(
                name="Binance Account",
                exchange=self.binance,
                api_key="account1_1234",
                secret="1234secret",
                token_pair=self.bnb,
                default=True,
            )
        response = update_balance(binance_account, update_price=False)
        self.assertEqual(response, [])
        self.assertEqual(mock_get_account.call_count, 1)
        self.assertEqual(mock_get_all_tickers.call_count, 0)

    @patch.object(Client, "get_all_tickers", autospec=True)
    @patch(
        "binance.client.Client.get_account",
        return_value=account_mock_dict_empty_balance,
    )  # noqa
    def test_account_update_balance_empty_binance_price(
        self, mock_get_account, mock_get_all_tickers
    ):
        with patch("vanir.core.account.helpers.balance.update_balance"):
            binance_account = Account.objects.create(
                name="Binance Account",
                exchange=self.binance,
                api_key="account1_1234",
                secret="1234secret",
                token_pair=self.bnb,
                default=True,
            )
        response = update_balance(binance_account, update_price=True)
        self.assertEqual(response, [])
        self.assertEqual(mock_get_account.call_count, 1)
        self.assertEqual(mock_get_all_tickers.call_count, 1)

    @patch.object(
        Client, "get_all_tickers", autospec=True, return_value=get_all_tickers_mock
    )
    @patch(
        "binance.client.Client.get_account",
        autospec=True,
        return_value=account_mock_dict,
    )  # noqa
    def test_account_update_balance_price_binance(
        self, mock_get_account, mock_get_all_tickers
    ):
        with patch("vanir.core.account.helpers.balance.update_balance"):
            binance_account = Account.objects.create(
                name="Binance Account",
                exchange=self.binance,
                api_key="account1_1234",
                secret="1234secret",
                token_pair=self.bnb,
                default=True,
            )
        response = update_balance(binance_account, update_price=True)
        self.assertEqual(response, ["EOS", "BNB", "LTC", "ETH", "BTC"])
        self.assertEqual(mock_get_account.call_count, 1)
        self.assertEqual(mock_get_all_tickers.call_count, 1)
