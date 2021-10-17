from django.db import models


class OrderSide(models.TextChoices):
    SIDE_BUY = "BUY"
    SIDE_SELL = "SELL"


class StopTakeType(models.TextChoices):
    ORDER_TYPE_STOP_LOSS = "STOP_LOSS"
    ORDER_TYPE_TAKE_PROFIT = "TAKE_PROFIT"


class LimitType(models.TextChoices):
    ORDER_TYPE_STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
    ORDER_TYPE_TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"


class TimeInForce(models.TextChoices):
    Good_Till_Cancel = "GTC"
    Immediate_Or_Cancel = "IOC"
    Fill_Or_Kill = "FOK"
