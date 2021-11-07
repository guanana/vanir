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
    """Orders abstract base model"""

    ORDER_TYPE = None
    order_id = models.CharField(max_length=150, editable=False)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, help_text=constants.ACCOUNT
    )
    token_from = models.ForeignKey(
        Token, related_name="token_from", on_delete=models.CASCADE, null=False
    )
    token_to = models.ForeignKey(
        Token, related_name="token_to", on_delete=models.CASCADE, null=False
    )
    side = models.CharField(
        max_length=4, choices=OrderSide.choices, null=False, default=OrderSide.SIDE_SELL
    )
    quoteOrderQty = models.FloatField(default=0.1, null=False)

    class Meta:
        unique_together = ["order_id", "account"]
        abstract = True

    @property
    def order_args(self):
        """
        To be implemented by child classes
        """
        raise NotImplementedError

    @property
    def base_order_args(self):
        """
        Base arguments common to all the types of orders
        """
        return {
            "symbol": self.symbol,
            "side": self.side,
            "type": self.ORDER_TYPE,
            "quantity": self.quoteOrderQty,
        }

    @property
    def symbol(self):
        """
        Construct symbol to send to exchange
        :return: Symbol
        :rtype: str
        """
        return f"{self.token_from.symbol}{self.token_to.symbol}"

    @property
    def new_client_order_id(self):
        """
        Construct order id to send to the exchange
        :return: datetime with symbol as identifier
        :rtype: str
        """
        return f"{datetime.datetime.today().strftime('%Y%m%d%H%M%S')}{self.symbol}"

    def save(self, *args, **kwargs):
        """
        Construct name and order id then send the order with the proper parameters
        :param args:
        :param kwargs:
        :return: save
        """
        self.name = f"{datetime.datetime.today().strftime('%X %x')}:{self.token_from.symbol}/{self.token_to.symbol}"
        self.order_id = self.new_client_order_id
        try:
            order = self.account.exchange_obj.create_order(
                **self.order_args, newClientOrderId=self.order_id
            )
            if not order:
                raise ValidationError(
                    "Order not able to process, please check the details"
                )
        except ValidationError as e:
            logger.error(e)
        return super(BaseOrder, self).save(*args, **kwargs)

    def execute_order(self, **kwargs):
        """
        Execute order on exchange
        :param kwargs:
        :return: response from exchange object
        """
        return self.account.exchange_obj.create_order(**self.order_args, **kwargs)

    @property
    def order_full_info(self):
        return self.account.exchange_obj.get_order(
            symbol=self.symbol, origClientOrderId=self.order_id
        )

    @property
    def order_status(self):
        try:
            return self.order_full_info["status"]
        except AttributeError:
            return


class BasePriceOrder(BaseOrder):
    """Order with price abstract base model"""
    price = models.FloatField(help_text=constants.PRICE, default=0)

    @property
    def order_args(self):
        add_on = {"price": self.price}
        base = self.base_order_args
        base.update(add_on)
        return base

    class Meta:
        abstract = True


class BasePriceLimitOrder(BasePriceOrder):
    """Base limit order abstract base model"""
    timeInForce = models.CharField(
        max_length=4,
        choices=TimeInForce.choices,
        default=TimeInForce.Good_Till_Cancel,
        help_text=constants.TIME_IN_FORCE,
    )

    class Meta:
        abstract = True


class LimitOrder(BasePriceLimitOrder):
    """Limit order model"""
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

    @staticmethod
    def get_title():
        return "Limit Order"

    @property
    def order_args(self):
        add_on = {"timeInForce": self.timeInForce, "price": self.price}
        base = self.base_order_args
        base.update(add_on)
        return base


class MarketOrder(BaseOrder):
    """Trade instantly at the current market price"""

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

    @staticmethod
    def get_title():
        return "Market Order"


class StopPriceOrder(BaseOrder):
    """Stop Price Order model"""
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
        add_on = {"stopPrice": self.stopprice}
        base = self.base_order_args
        base.update(add_on)
        return base

    @staticmethod
    def get_title():
        return "Stop Price Order"


class StopLossOrTakeProfitLimitOrder(BasePriceLimitOrder):
    """Stop Loos or Take Profit Order model"""
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
        add_on = {
            "price": self.price,
            "timeInForce": self.timeInForce,
            "stopPrice": self.stopprice,
        }
        base = self.base_order_args
        base.update(add_on)
        return base

    @staticmethod
    def get_title():
        return "Stop Loss Or Take Profit Limit Order"
