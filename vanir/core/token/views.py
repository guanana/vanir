from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from vanir.core.token.filtersets import TokenFilter
from vanir.core.token.helpers.import_utils import bulk_update
from vanir.core.token.models import Token
from vanir.core.token.tables import TokenTable
from vanir.utils.views import (
    ObjectCreateView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListFilterView,
    ObjectListView,
    ObjectUpdateView,
)


class TokenCreateView(ObjectCreateView):
    model = Token
    fields = ("name", "symbol", "blockchain", "last_value")


class TokenListView(ObjectListFilterView):
    model = Token
    table_class = TokenTable
    filterset_class = TokenFilter


class TokenUpdateView(ObjectUpdateView):
    model = Token


class TokenDetailView(ObjectDetailView):
    model = Token


class TokenDeleteView(ObjectDeleteView):
    model = Token
    success_url = reverse_lazy("token:token_list")


class TokenDetailUpdateValueView(ObjectDetailView):
    model = Token

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object.set_value()
        return redirect(reverse("token:token_detail", kwargs={"pk": self.object.pk}))


class TokenBulkUpdateValueView(ObjectListView):
    model = Token
    table_class = TokenTable

    def get(self, request, *args, **kwargs):
        bulk_update()
        messages.info(request, "Bulk update completed")
        return super(TokenBulkUpdateValueView, self).get(request, *args, **kwargs)
