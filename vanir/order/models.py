import datetime
import logging

from django.core.exceptions import ValidationError
from django.db import models

from vanir.core.account.models import Account
from vanir.core.token.models import Token
from vanir.utils.models import BaseObject

from . import constants
from .choices import LimitType, OrderSide, StopTakeType, TimeInForce

logger = logging.getLogger(__name__)


class BaseOrder(BaseObject):
    """
    Orders
    """

    ORDER_TYPE = None
    order_id = models.CharField(max_length=250, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    token_from = models.ForeignKey(
        Token, related_name="token_from", on_delete=models.CASCADE, null=False
    )
    token_to = models.ForeignKey(
        Token, related_name="token_to", on_delete=models.CASCADE, null=False
    )
    side = models.CharField(max_length=4, choices=OrderSide.choices, null=False)
    quoteOrderQty = models.FloatField(default=0.1, null=False)

    class Meta:
        unique_together = ["order_id", "account"]
        abstract = True

    @property
    def order_args(self):
        raise NotImplementedError

    @property
    def base_order_args(self):
        return {
            "symbol": self.symbol,
            "side": self.side,
            "type": self.ORDER_TYPE,
            "quantity": self.quoteOrderQty,
        }

    @property
    def symbol(self):
        return f"{self.token_from.symbol}{self.token_to.symbol}"

    @property
    def new_client_order_id(self):
        return f"{datetime.datetime.today()}{self.symbol}"

    def save(self, *args, **kwargs):
        self.name = f"{datetime.datetime.today().strftime('%X %x')}:{self.token_from.symbol}/{self.token_to.symbol}"
        self.orden_id = self.new_client_order_id
        try:
            test = self.account.exchange_obj.test_order(**self.order_args)  # noqa F841
        except ValidationError as e:
            logger.error(e)
        super().save(*args, **kwargs)

    def execute_order(self, **kwargs):
        return self.account.exchange_obj.create_order(**self.order_args, **kwargs)

    # def test_order(self, **kwargs):
    #     return self.account.exchange_obj.create_test_order(**self.order_args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("order:order_detail", kwargs={"pk": self.pk})


class BasePriceOrder(BaseOrder):
    price = models.FloatField(help_text=constants.PRICE, default=0)

    @property
    def order_args(self):
        self.base_order_args.update({"price": self.price})
        return self.base_order_args

    class Meta:
        abstract = True


class BasePriceLimitOrder(BasePriceOrder):
    timeInForce = models.CharField(
        max_length=4,
        choices=TimeInForce.choices,
        default=TimeInForce.Good_Till_Cancel,
        help_text=constants.TIME_IN_FORCE,
    )

    class Meta:
        abstract = True

    @property
    def order_args(self):
        self.base_order_args.update(
            {"price": self.price, "timeInForce": self.timeInForce}
        )
        return self.base_order_args

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("order:limitorder_detail", kwargs={"pk": self.pk})


class LimitOrder(BasePriceLimitOrder):
    ORDER_TYPE = "LIMIT"
    token_from = models.ForeignKey(
        Token, related_name="token_from_limit", on_delete=models.CASCADE, null=False
    )
    token_to = models.ForeignKey(
        Token,
        related_name="token_to_limit",
        on_delete=models.CASCADE,
        null=False,
    )


class MarketOrder(BaseOrder):
    """
    Trade instantly at the current market price
    """

    ORDER_TYPE = "MARKET"
    token_from = models.ForeignKey(
        Token, related_name="token_from_market", on_delete=models.CASCADE, null=False
    )
    token_to = models.ForeignKey(
        Token,
        related_name="token_to_market",
        on_delete=models.CASCADE,
        null=False,
    )

    @property
    def order_args(self):
        return self.base_order_args


class StopPriceOrder(BaseOrder):
    stopprice = models.FloatField(help_text=constants.PRICE, default=0)
    token_from = models.ForeignKey(
        Token,
        related_name="token_from_stop_price",
        on_delete=models.CASCADE,
        null=False,
    )
    token_to = models.ForeignKey(
        Token,
        related_name="token_to_stop_price",
        on_delete=models.CASCADE,
        null=False,
    )
    ORDER_TYPE = models.CharField(
        max_length=30, choices=StopTakeType.choices, help_text=constants.ORDER_TAKE_STOP
    )

    @property
    def order_args(self):
        self.base_order_args.update({"stopPrice": self.stopprice})
        return self.base_order_args

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("order:stoplossortakeprofitorder_detail", kwargs={"pk": self.pk})


class StopLossOrTakeProfitLimitOrder(BasePriceLimitOrder):
    token_from = models.ForeignKey(
        Token,
        related_name="token_from_loss_or_take",
        on_delete=models.CASCADE,
        null=False,
    )
    token_to = models.ForeignKey(
        Token,
        related_name="token_to_loss_or_take",
        on_delete=models.CASCADE,
        null=False,
    )
    stopprice = models.FloatField(help_text=constants.STOPPRICE, default=0)
    ORDER_TYPE = models.CharField(
        max_length=30, choices=LimitType.choices, help_text=constants.ORDER_TAKE_STOP
    )

    @property
    def order_args(self):
        self.base_order_args.update(
            {
                "price": self.price,
                "timeInForce": self.timeInForce,
                "stopPrice": self.stopprice,
            }
        )
        return self.base_order_args

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse(
            "order:stoplossortakeprofitlimitorder_detail", kwargs={"pk": self.pk}
        )
