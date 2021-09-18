from django.urls import reverse_lazy

from vanir.token.models import Token
from vanir.token.tables import TokenTable
from vanir.utils.views import ObjectListView, ObjectUpdateView, ObjectDetailView, ObjectDeleteView, ObjectCreateView


class TokenCreateView(ObjectCreateView):
    model = Token
    fields = ("name", "symbol", "blockchain", "decimals")


class TokenListView(ObjectListView):
    model = Token
    table_class = TokenTable


class TokenUpdateView(ObjectUpdateView):
    model = Token


class TokenDetailView(ObjectDetailView):
    model = Token


class TokenDeleteView(ObjectDeleteView):
    model = Token
    success_url = reverse_lazy("token:token_list")
