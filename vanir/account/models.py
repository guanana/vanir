from decimal import Decimal

from django.db import models

from vanir.exchange.models import Exchange
from vanir.users.admin import User
from binance.client import Client
from binance.exceptions import BinanceAPIException

from vanir.utils.models import BaseObject


class Account(BaseObject):
    """
    Exchange Account
    """
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=250)
    secret = models.CharField(max_length=250)
    tld = models.CharField(max_length=10, default="com")
    password = models.CharField(max_length=250, blank=True, null=True)
    default_fee_rate = models.DecimalField(
        max_digits=30, decimal_places=4, default=0.01
    )
    @property
    def name(self):
        return f"{self.pk:02}-{self.exchange}-{self.user.get_username()}"

    @property
    def get_account_client(self):
        return Client(api_key=self.api_key, api_secret=self.secret, tld=self.tld)
