from django.urls import reverse_lazy

from vanir.core.blockchain.models import Blockchain
from vanir.core.blockchain.tables import BlockchainTable
from vanir.utils.views import (
    ObjectCreateView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListView,
    ObjectUpdateView,
)


class BlockchainCreateView(ObjectCreateView):
    model = Blockchain
    fields = ("name", "project_url", "explorer_url")


class BlockchainListView(ObjectListView):
    model = Blockchain
    table_class = BlockchainTable


class BlockchainUpdateView(ObjectUpdateView):
    model = Blockchain


class BlockchainDetailView(ObjectDetailView):
    model = Blockchain


class BlockchainDeleteView(ObjectDeleteView):
    model = Blockchain
    success_url = reverse_lazy("blockchain:blockchain_list")
