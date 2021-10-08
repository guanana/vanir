from django.urls import reverse_lazy

from vanir.utils.views import (
    ObjectCreateView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListView,
)

from .models import (
    LimitOrder,
    MarketOrder,
    StopLossOrTakeProfitLimitOrder,
    StopPriceOrder,
)
from .tables import (
    LimitOrderTable,
    MarketOrderTable,
    StopLossOrTakeProfitLimitOrderTable,
    StopPriceOrderTable,
)


###
# LimitOrder
###
class LimitOrderCreateView(ObjectCreateView):
    model = LimitOrder
    fields = (
        "account",
        "token_from",
        "token_to",
        "side",
        "quoteOrderQty",
        "timeInForce",
    )
    # TODO: Explore django-autocomplete-light to filter token_from


class LimitOrderListView(ObjectListView):
    model = LimitOrder
    table_class = LimitOrderTable


class LimitOrderDetailView(ObjectDetailView):
    model = LimitOrder
    template_name = "order/order_detail.html"
    table_class = LimitOrderTable


class LimitOrderDeleteView(ObjectDeleteView):
    model = LimitOrder
    success_url = reverse_lazy("order:limitorder_list")


###
# MarketOrder
###
class MarketOrderCreateView(ObjectCreateView):
    model = MarketOrder
    fields = ("account", "token_from", "token_to", "side", "quoteOrderQty")


class MarketOrderListView(ObjectListView):
    model = MarketOrder
    table_class = MarketOrderTable


class MarketOrderDetailView(ObjectDetailView):
    model = MarketOrder


class MarketOrderDeleteView(ObjectDeleteView):
    model = MarketOrder
    success_url = reverse_lazy("order:marketorder_list")


###
# StopPriceOrder
###
class StopPriceOrderCreateView(ObjectCreateView):
    model = StopPriceOrder
    fields = (
        "account",
        "token_from",
        "token_to",
        "side",
        "ORDER_TYPE",
        "quoteOrderQty",
        "stopprice",
    )


class StopPriceOrderListView(ObjectListView):
    model = StopPriceOrder
    table_class = StopPriceOrderTable


class StopPriceOrderDetailView(ObjectDetailView):
    model = StopPriceOrder


class StopPriceOrderDeleteView(ObjectDeleteView):
    model = StopPriceOrder
    success_url = reverse_lazy("order:stoppriceorder_list")


###
# StopLossOrTakeProfitLimitOrder
###
class StopLossOrTakeProfitLimitOrderCreateView(ObjectCreateView):
    model = StopLossOrTakeProfitLimitOrder
    fields = (
        "account",
        "token_from",
        "token_to",
        "side",
        "ORDER_TYPE",
        "quoteOrderQty",
        "stopprice",
    )


class StopLossOrTakeProfitLimitOrderListView(ObjectListView):
    model = StopLossOrTakeProfitLimitOrder
    table_class = StopLossOrTakeProfitLimitOrderTable


class StopLossOrTakeProfitLimitOrderDetailView(ObjectDetailView):
    model = StopLossOrTakeProfitLimitOrder


class StopLossOrTakeProfitLimitOrderDeleteView(ObjectDeleteView):
    model = StopLossOrTakeProfitLimitOrder
    success_url = reverse_lazy("order:stoplossortakeprofitlimitorder_list")
