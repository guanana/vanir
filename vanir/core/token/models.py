from django.db import models

from vanir.core.token.choices import TokenTypes
from vanir.utils.models import BaseObject


class Coin(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    last_value = models.FloatField(null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.symbol

    def natural_key(self):
        return (self.symbol,)

    def set_value(self, account=None):
        from vanir.utils.helpers import fetch_default_account, value_pair

        if not account:
            account = fetch_default_account()
        exceptions_value = self.check_exceptions_value(account)
        if exceptions_value:
            return exceptions_value
        self.last_value = account.exchange_obj.get_token_price(
            value_pair(self, account.token_pair)
        )
        if self.last_value:
            self.last_value = round(self.last_value, 4)
            self.save()
            return self.last_value
        else:
            return False

    def check_exceptions_value(self, account):
        dollar_pairs = ("BUSD", "USDT", "USDC", "DAI", "UST", "TUSD", "USDP")
        # Special exception when calling same pair
        if self.symbol == account.token_pair.symbol:
            self.last_value = 1
            self.save()
            return 1
        elif self.symbol in dollar_pairs and account.token_pair.symbol in dollar_pairs:
            self.last_value = 1
            self.save()
            return 1


class Token(BaseObject, Coin):
    token_type = models.CharField(max_length=9, choices=TokenTypes.choices, null=True)

    class Meta:
        unique_together = ("name", "symbol")

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("token:token_detail", kwargs={"pk": self.pk})
