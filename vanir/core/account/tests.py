from unittest.mock import patch

import pytest
from binance.exceptions import BinanceAPIException
from django.test import TestCase
from django.urls import resolve, reverse

from vanir.core.account.helpers.test_helpers import aux_create_basic_account
from vanir.core.account.models import Account, AccountTokens
from vanir.core.exchange.models import Exchange
from vanir.core.token.models import Token


class AccountModelTest(TestCase):
    def setUp(self):
        self.token = Token.objects.create(name="Test", symbol="TST")
        self.exchange = Exchange.objects.create(
            name="exchange_test", native_token=self.token
        )
        self.bnb = Token.objects.create(symbol="BNB", name="Binance Coin")
        self.binance = Exchange.objects.create(name="Binance", native_token=self.bnb)

    def test_create_account(self):
        account_create = aux_create_basic_account(
            name="account1", exchange=self.exchange, token_pair=self.token
        )
        account_get = Account.objects.get(exchange=self.exchange.id)
        self.assertEqual(account_create, account_get)

    def test_default_account_auto_change(self):
        account1 = aux_create_basic_account(
            name="account1", exchange=self.exchange, token_pair=self.token
        )
        self.assertEqual(account1.default, True)
        account2 = aux_create_basic_account(
            name="account2", exchange=self.exchange, token_pair=self.token
        )
        account1.refresh_from_db()
        account2.refresh_from_db()
        self.assertEqual(account1.default, False)
        self.assertEqual(account2.default, True)

    def test_add_tokens(self):
        account1 = aux_create_basic_account(
            name="account1", exchange=self.exchange, token_pair=self.token
        )
        test_token = Token.objects.create(
            symbol="ADDTKN", name="Add Tokens", last_value=5.34242
        )
        AccountTokens.objects.create(account=account1, token=test_token, quantity=2)
        self.assertEqual(account1.total_value_account, 10.6848)

    def test_supported_exchange_binance_no_valid_key(self):
        with pytest.raises(BinanceAPIException):
            account1 = aux_create_basic_account(  # noqa F841
                name="account1", exchange=self.binance, token_pair=self.token
            )

    @patch("vanir.core.account.helpers.balance.update_balance")
    def test_supported_exchange_binance(self, mock_balance):
        account1 = aux_create_basic_account(
            name="account1", exchange=self.binance, token_pair=self.token
        )
        self.assertEqual(account1.extended_exchange, True)
        self.assertEqual(mock_balance.called, True)

    @patch("vanir.core.account.helpers.balance.update_balance")
    def test_manual_exchange(self, mock_balance):
        account1 = aux_create_basic_account(
            name="account1", exchange=self.exchange, token_pair=self.token
        )
        self.assertEqual(account1.extended_exchange, False)
        self.assertEqual(mock_balance.called, True)


class TestAccountUrls(TestCase):
    def setUp(self):
        self.token = Token.objects.create(name="Test", symbol="TST")
        self.exchange = Exchange.objects.create(
            name="exchange_test", native_token=self.token
        )
        self.account = aux_create_basic_account(
            name="account1", exchange=self.exchange, token_pair=self.token
        )

    def url_test(self, url_name, args: dict = None):
        app_label = self.account._meta.app_label
        class_name = self.account.__class__.__name__.lower()
        if args:
            path = reverse(f"{app_label}:{class_name}_{url_name}", kwargs=args)
        else:
            path = reverse(f"{app_label}:{class_name}_{url_name}")
        return path

    def test_list_account_url(self):
        path = self.url_test("list")
        assert resolve(path).view_name == "account:account_list"

    def test_add_account_url(self):
        path = self.url_test("add")
        assert resolve(path).view_name == "account:account_add"

    def test_detail_account_url(self):
        path = self.url_test("detail", {"pk": 1})
        assert resolve(path).view_name == "account:account_detail"

    def test_edit_account_url(self):
        path = self.url_test("edit", {"pk": 1})
        assert resolve(path).view_name == "account:account_edit"

    def test_tokens_add_account_url(self):
        path = self.url_test("tokens_add", {"pk": 1})
        assert resolve(path).view_name == "account:account_tokens_add"

    def test_delete_account_url(self):
        path = self.url_test("delete", {"pk": 1})
        assert resolve(path).view_name == "account:account_delete"

    def test_refresh_account_url(self):
        path = self.url_test("refresh", {"pk": 1})
        assert resolve(path).view_name == "account:account_refresh"

    def test_test_account_url(self):
        path = self.url_test("test", {"pk": 1})
        assert resolve(path).view_name == "account:account_test"

    def test_delete_tokens_account_url(self):
        path = self.url_test("delete_tokens", {"pk": 1})
        assert resolve(path).view_name == "account:account_delete_tokens"

    def test_balance_import_account_url(self):
        path = self.url_test("balance_import", {"pk": 1})
        assert resolve(path).view_name == "account:account_balance_import"

    def test_more_account_url(self):
        path = self.url_test("more", {"pk": 1})
        assert resolve(path).view_name == "account:account_more"
