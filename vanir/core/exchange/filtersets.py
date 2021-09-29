import django_filters
from django_filters import FilterSet

from vanir.core.blockchain.models import Blockchain
from vanir.core.exchange.models import Exchange


class ExchangeFilterSet(FilterSet):
    blockchain_id = django_filters.ModelMultipleChoiceFilter(
        field_name="default_blockchain",
        queryset=Blockchain.objects.all(),
        label="Blockchain (ID)",
    )
    blockchain = django_filters.ModelMultipleChoiceFilter(
        field_name="default_blockchain__name",
        queryset=Blockchain.objects.all(),
        to_field_name="name",
        label="Blockchain (Name)",
    )

    class Meta:
        model = Exchange
        fields = ["id", "name"]
