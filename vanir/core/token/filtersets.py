from django_filters import FilterSet

from vanir.core.token.models import Token


class TokenFilter(FilterSet):
    class Meta:
        model = Token
        fields = ["name", "symbol", "last_value"]
