# from unittest.mock import patch
#
# from django.test import TestCase
#
# from vanir.core.account.helpers.balance import update_balance
# from vanir.core.account.helpers.test_helpers import aux_create_basic_account
# from vanir.core.account.models import Account
# from vanir.core.exchange.models import Exchange
# from vanir.core.token.models import Token


# account_mock_dict = {
#     "makerCommission": 10,
#     "takerCommission": 10,
#     "buyerCommission": 0,
#     "sellerCommission": 0,
#     "canTrade": True,
#     "canWithdraw": True,
#     "canDeposit": True,
#     "updateTime": 1635129047375,
#     "accountType": "SPOT",
#     "balances": [
#         {"asset": "BTC", "free": "0.00014051", "locked": "0.00000000"},
#         {"asset": "LTC", "free": "0.01530277", "locked": "0.07693000"},
#         {"asset": "ETH", "free": "0.00401792", "locked": "0.00000000"},
#         {"asset": "NEO", "free": "0.00000000", "locked": "0.00000000"},
#         {"asset": "BNB", "free": "0.09387603", "locked": "0.00000000"},
#         {"asset": "QTUM", "free": "0.00000000", "locked": "0.00000000"},
#         {"asset": "EOS", "free": "10.64085300", "locked": "10.00000000"},
#         {"asset": "SNT", "free": "0.00000000", "locked": "0.00000000"},
#         {"asset": "BCC", "free": "0.00000000", "locked": "0.00000000"},
#         {"asset": "USDT", "free": "0.00000000", "locked": "0.00000000"},
#         {"asset": "HSR", "free": "0.00000000", "locked": "0.00000000"},
#     ],
#     "permissions": ["SPOT"],
# }
# get_margin_all_assets_mock_dict = [
#     {
#         "assetFullName": "USD coin",
#         "assetName": "USDC",
#         "isBorrowable": True,
#         "isMortgageable": True,
#         "userMinBorrow": "0.00000000",
#         "userMinRepay": "0.00000000"
#     },
#     {
#         "assetFullName": "BNB-coin",
#         "assetName": "BNB",
#         "isBorrowable": True,
#         "isMortgageable": True,
#         "userMinBorrow": "1.00000000",
#         "userMinRepay": "0.00000000"
#     },
#     {
#         "assetFullName": "Etherum",
#         "assetName": "ETH",
#         "isBorrowable": True,
#         "isMortgageable": True,
#         "userMinBorrow": "1.00000000",
#         "userMinRepay": "0.00000000"
#     }
# ]

# TODO: Implement tests
# class TestVanirBinance(TestCase):
#     def setUp(self):
#         self.bnb = Token.objects.create(symbol="BNB", name="Binance Coin")
#         self.binance = Exchange.objects.create(name="Binance", native_token=self.bnb)
#
#     @patch("binance.client.Client.ping")
#     @patch("binance.client.Client.get_account", return_value=account_mock_dict)  # noqa
#     def test_account_get_balance_binance(self, mock_binance, mock_get_account):
#         binance_account = Account.objects.create(
#             name="Binance Account",
#             exchange=self.binance,
#             api_key="account1_1234",
#             secret="1234secret",
#             token_pair=self.bnb,
#             default=True,
#         )
#         df = binance_account.exchange_obj.get_balance()
#         self.assertIsNone(df)
