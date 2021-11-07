from vanir.utils.tables import ObjectTable

from .models import LimitOrder, MarketOrder, StopLossOrTakeProfitLimitOrder, StopPriceOrder


class LimitOrderTable(ObjectTable):
    class Meta:
        model = LimitOrder
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "name",
            "account",
            "token_from",
            "token_to",
            "side",
            "quoteOrderQty",
            "price",
            "timeInForce",
            "order_status",
        )


class MarketOrderTable(ObjectTable):
    class Meta:
        model = MarketOrder
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "name",
            "account",
            "token_from",
            "token_to",
            "side",
            "quoteOrderQty",
            "order_status",
        )


class StopPriceOrderTable(ObjectTable):
    class Meta:
        model = StopPriceOrder
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "name",
            "account",
            "token_from",
            "token_to",
            "side",
            "ORDER_TYPE",
            "quoteOrderQty",
            "stopprice",
            "order_status",
        )


class StopLossOrTakeProfitLimitOrderTable(ObjectTable):
    class Meta:
        model = StopLossOrTakeProfitLimitOrder
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "name",
            "account",
            "token_from",
            "token_to",
            "side",
            "quoteOrderQty",
            "ORDER_TYPE",
            "timeInForce",
            "price",
            "stopprice",
            "order_status",
        )
