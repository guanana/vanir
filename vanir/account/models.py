from decimal import Decimal

from django.db import models

from vanir.exchange.models import Exchange
from vanir.users.admin import User
from binance.client import Client
from binance.exceptions import BinanceAPIException


class Account(models.Model):
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
        max_digits=30, decimal_places=4, default=Decimal(0.1)
    )

    @property
    def get_account_client(self):
        return Client(api_key=self.api_key, api_secret=self.secret, tld=self.tld)

    def __str__(self):
        return f"{self.pk}: {self.exchange} - {self.user.get_username()}"
