from django.db import models

from vanir.blockchain.models import Blockchain
from vanir.token.choices import TokenTypes
from vanir.utils.models import BaseObject


class Coin(BaseObject):
    name = models.CharField(max_length=40)
    symbol = models.CharField(max_length=6)
    blockchain = models.ForeignKey(Blockchain, on_delete=models.CASCADE)
    last_value = models.FloatField(null=True)

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
        self.last_value = account.exchange_obj.get_token_price(
            f"{self.symbol}{account.token_pair}"
        )
        self.save()
        return self.last_value


class Token(Coin):
    token_type = models.CharField(max_length=9, choices=TokenTypes.choices)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("token:token_detail", kwargs={"pk": self.pk})
