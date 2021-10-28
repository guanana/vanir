import django_filters
from django_filters import FilterSet

from vanir.core.account.models import Account


class AccountFilterSet(FilterSet):
    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    class Meta:
        model = Account
        fields = {
            "name": ["icontains"],
            "api_key": ["iexact"],
            "secret": ["iexact"],
            "tld": ["iexact"],
            "default": ["exact"],
            "testnet": ["exact"],
        }
