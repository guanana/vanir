import django_filters

from vanir.core.token.models import Token


class TokenFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    symbol = django_filters.CharFilter(lookup_expr="icontains")
    last_value = django_filters.NumberFilter(
        lookup_expr="gte", label="Last value greater than"
    )

    class Meta:
        model = Token
        fields = ["name", "symbol", "last_value"]
