from django_filters import FilterSet

from vanir.order.models import LimitOrder, MarketOrder, StopLossOrTakeProfitLimitOrder, StopPriceOrder


class BaseFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super(BaseFilter, self).__init__(*args, **kwargs)
        self.filters["account"].label = "Account"
        # TODO: Check why not working, probably name vs symbol?
        # self.filters['token_to'].label = "Token To"
        # self.filters['token_from'].label = "Token From"
        self.filters["side"].label = "Side"

    class Meta:
        model = None
        fields = ["name", "account", "side"]


class LimitOrderFilter(BaseFilter):
    class Meta(BaseFilter.Meta):
        model = LimitOrder


class MarketOrderFilter(BaseFilter):
    class Meta(BaseFilter.Meta):
        model = MarketOrder


class StopPriceOrderFilter(BaseFilter):
    class Meta(BaseFilter.Meta):
        model = StopPriceOrder


class StopLossOrTakeProfitLimitOrderFilter(BaseFilter):
    class Meta(BaseFilter.Meta):
        model = StopLossOrTakeProfitLimitOrder
