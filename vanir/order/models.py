import datetime

from django.db import models

from vanir.core.account.models import Account
from vanir.core.token.models import Token

from .choices import OrderSide, OrderType


class Order(models.Model):
    """
    Orders
    """

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    token_from = models.ForeignKey(
        Token, related_name="token_from", on_delete=models.CASCADE, null=False
    )
    token_to = models.ForeignKey(
        Token, related_name="token_to", on_delete=models.CASCADE, null=False
    )
    side = models.CharField(max_length=4, choices=OrderSide.choices, null=False)
    orderType = models.CharField(max_length=20, choices=OrderType.choices, null=False)
    quoteOrderQty = models.FloatField(default=0.1, null=False)

    # stopLossQty = models.DecimalField(
    #     max_digits=30, decimal_places=8, default=Decimal(0.1)
    # )
    # stopPrice = models.DecimalField(
    #     max_digits=30, decimal_places=8, default=Decimal(0.1)
    # )
    #
    # takeProfitQty = models.DecimalField(
    #     max_digits=30, decimal_places=8, default=Decimal(0.1)
    # )
    # takeProfitPrice = models.DecimalField(
    #     max_digits=30, decimal_places=8, default=Decimal(0.1)
    # )

    @property
    def symbol(self):
        return f"{self.token_from}{self.token_to}"

    def save(self, *args, **kwargs):
        self.name = f"{datetime.datetime.today()}:{self.symbol}"
        super().save(*args, **kwargs)

    def get_avg_price(self):
        return self.account.get_account_client.get_avg_price(symbol=self.symbol)

    def execute_order(self, **kwargs):
        return self.account.get_account_client.create_order(
            symbol=self.symbol,
            side=self.side,
            type=self.orderType,
            quantity=self.quoteOrderQty,
            **kwargs,
        )

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("order:order_detail", kwargs={"pk": self.pk})
