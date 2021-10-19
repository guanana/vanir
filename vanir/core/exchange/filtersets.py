from django_filters import FilterSet

from vanir.core.exchange.models import Exchange


class ExchangeFilterSet(FilterSet):
    class Meta:
        model = Exchange
        fields = ["id", "name"]
