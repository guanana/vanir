from unittest.mock import patch

from django.test import TestCase

from vanir.core.account.helpers.test_helpers import aux_create_basic_account
from vanir.core.exchange.models import Exchange
from vanir.core.token.models import Token


class TestAccountHelpers(TestCase):
    def setUp(self):
        self.token = Token.objects.create(name="Test Helper", symbol="TSTHELP")
        self.manual_exchange = Exchange.objects.create(
            name="exchange_test", native_token=self.token
        )
        self.manual_account = aux_create_basic_account(
            name="account1", exchange=self.manual_exchange, token_pair=self.token
        )

    @patch("vanir.utils.datasource.coingecko.CoinGeckoVanir.get_coins_markets")
    def test_account_get_balance_manual(self, mock_coingecko_price):
        df = self.manual_account.exchange_obj.get_balance()
        self.assertIsNone(df)
        self.assertEqual(mock_coingecko_price.called, False)
