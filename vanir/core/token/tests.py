from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from vanir.core.token.models import Token


class TokenViewTestNoAuth(TestCase):
    def setUp(self):
        self.token = Token.objects.create(name="Test", symbol="TST")

    def test_view_url_no_auth(self):
        url = "/token/"
        response = self.client.get(url)
        login = "/users/login/?next="
        self.assertEqual(response.status_code, 302)
        self.assertEqual(f"{login}{url}", f"{login}{response.request['PATH_INFO']}")

    def test_view_url_accessible_by_pk_no_auth(self):
        pk = Token.objects.get(name="Test").pk
        url = reverse('token:token_detail', args=[pk])
        response = self.client.get(url)
        login = "/users/login/?next="
        self.assertEqual(response.status_code, 302)
        self.assertEqual(f"{login}{url}", f"{login}{response.request['PATH_INFO']}")


class ExchangeViewTestAuth(TestCase):
    def setUp(self):
        self.token = Token.objects.create(name="Test", symbol="TST")
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', "admin")

    def test_view_url_auth(self):
        self.client.logout()
        url = "/token/"
        login = self.client.login(username=self.admin_user.username, password='admin')
        response = self.client.get(url)
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_pk_auth(self):
        self.client.logout()
        pk = Token.objects.get(name="Test").pk
        url = reverse('token:token_detail', args=[pk])
        login = self.client.login(username=self.admin_user.username, password='admin')
        response = self.client.get(url)
        self.assertEqual(login, True)
        self.assertEqual(response.status_code, 200)
