from django_filters import FilterSet

from vanir.core.blockchain.models import Blockchain


class BlockchainFilterSet(FilterSet):
    class Meta:
        model = Blockchain
        fields = ["id", "name", "project_url", "explorer_url"]
