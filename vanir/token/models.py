from binance.exceptions import BinanceAPIException
from django.db import models

from vanir.blockchain.models import Blockchain
from vanir.token.choices import TokenTypes
from vanir.utils.models import BaseObject


class Coin(BaseObject):
    name = models.CharField(max_length=40)
    symbol = models.CharField(max_length=6)
    blockchain = models.ForeignKey(Blockchain, on_delete=models.CASCADE)
    last_value = models.DecimalField(decimal_places=10, max_digits=40, null=True)

    def __str__(self):
        return self.symbol

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("token:coin_detail", kwargs={"pk": self.pk})

    def get_value(self, account=None):
        if not account:
            from vanir.utils.helpers import fetch_default_account

            account = fetch_default_account()

        # Special exception when calling same pair
        if self.symbol == account.token_pair:
            return 0

        from vanir.account.utils import get_exchange

        exchange_obj = get_exchange(account.pk)
        try:
            price = exchange_obj.con.get_avg_price(
                symbol=f"{self.symbol}{account.token_pair}"
            )["price"]
        except BinanceAPIException as binanceexception:
            if binanceexception.code == -1121:
                raise ValueError(
                    f"Pair {self.symbol}{account.token_pair} not supported"
                )

        try:
            self.last_value = float(price)
        except ValueError:
            raise ValueError("Something went wrong, try again later")
        self.save()
        return self.last_value


class Token(Coin):
    token_type = models.CharField(max_length=9, choices=TokenTypes.choices)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("token:token_detail", kwargs={"pk": self.pk})
