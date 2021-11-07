from django.urls import reverse_lazy

from vanir.core.exchange.models import Exchange
from vanir.core.exchange.tables import ExchangeTable
from vanir.utils.views import ObjectCreateView, ObjectDeleteView, ObjectDetailView, ObjectListView, ObjectUpdateView


class ExchangeCreateView(ObjectCreateView):
    model = Exchange
    fields = ("name", "default_fee", "native_token")


class ExchangeListView(ObjectListView):
    model = Exchange
    table_class = ExchangeTable


class ExchangeUpdateView(ObjectUpdateView):
    model = Exchange


class ExchangeDetailView(ObjectDetailView):
    model = Exchange
    table_class = ExchangeTable


class ExchangeDeleteView(ObjectDeleteView):
    model = Exchange
    success_url = reverse_lazy("exchange:exchange_list")
