from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from vanir.core.exchange.models import Exchange
from vanir.core.token.models import Token


class ExchangeViewTestNoAuth(TestCase):
    def setUp(self):
        self.token = Token.objects.create(name="Test", symbol="TST")
        self.exchange = Exchange.objects.create(
            name="exchange_test", native_token=self.token
        )

    def test_view_url_no_auth(self):
        url = "/exchange/"
        response = self.client.get(url)
        login = "/users/login/?next="
        self.assertEqual(response.status_code, 302)
        self.assertEqual(f"{login}{url}", f"{login}{response.request['PATH_INFO']}")

    def test_view_url_accessible_by_pk_no_auth(self):
        pk = Exchange.objects.get(name="exchange_test").pk
        url = reverse('exchange:exchange_detail', args=[pk])
        response = self.client.get(url)
        login = "/users/login/?next="
        self.assertEqual(response.status_code, 302)
        self.assertEqual(f"{login}{url}", f"{login}{response.request['PATH_INFO']}")


class ExchangeViewTestAuth(TestCase):
    def setUp(self):
        self.token = Token.objects.create(name="Test", symbol="TST")
        self.exchange = Exchange.objects.create(
            name="exchange_test", native_token=self.token
        )
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', "admin")

    def test_view_url_auth(self):
        self.client.logout()
        url = "/exchange/"
        login = self.client.login(username=self.admin_user.username, password='admin')
        response = self.client.get(url)
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_pk_auth(self):
        self.client.logout()
        pk = Exchange.objects.get(name="exchange_test").pk
        url = reverse('exchange:exchange_detail', args=[pk])
        login = self.client.login(username=self.admin_user.username, password='admin')
        response = self.client.get(url)
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
