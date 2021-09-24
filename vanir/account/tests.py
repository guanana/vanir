from django.contrib.auth.models import User
from django.test import TestCase

from vanir.account.models import Account
from vanir.blockchain.models import Blockchain
from vanir.exchange.models import Exchange
from vanir.token.models import Token


class AccountModelTest(TestCase):
    def setUp(self):
        self.blockchain = Blockchain.objects.create(name="TestBlockchain")
        self.token = Token.objects.create(
            name="Test", symbol="TST", blockchain=self.blockchain
        )
        self.exchange = Exchange.objects.create(
            name="exchange_test", native_token=self.token
        )
        self.user = User.objects.create(username="user_test")
        self.account = Account.objects.create(
            exchange=self.exchange,
            user=self.user,
            api_key="account1_1234",
            secret="1234secret",
            token_pair=self.token,
            default=True,
        )

    def test_createaccount(self):
        account = Account.objects.get(exchange=self.exchange.id, user=self.user.id)
        self.assertEqual(self.account, account)

    def test_defaultaccount(self):
        self.account2 = Account.objects.create(
            exchange=self.exchange,
            user=self.user,
            api_key="account2_1234",
            secret="1234secret",
            token_pair=self.token,
            default=True,
        )
        self.account.refresh_from_db()
        self.assertEqual(self.account.default, False)
        self.assertEqual(self.account2.default, True)
