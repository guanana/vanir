from django.contrib.auth.models import User
from django.test import TestCase

from vanir.core.account.models import Account
from vanir.core.exchange.models import Exchange
from vanir.core.token.models import Token


class AccountModelTest(TestCase):
    def setUp(self):
        self.token = Token.objects.create(name="Test", symbol="TST")
        self.exchange = Exchange.objects.create(
            name="exchange_test", native_token=self.token
        )
        self.user = User.objects.create(username="user_test")
        self.account = Account.objects.create(
            name="account1",
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
            name="account2",
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
