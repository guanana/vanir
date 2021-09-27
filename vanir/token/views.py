from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from vanir.token.helpers.import_utils import bulk_update
from vanir.token.models import Token
from vanir.token.tables import TokenTable
from vanir.utils.views import (
    ObjectCreateView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListView,
    ObjectUpdateView,
)


class TokenCreateView(ObjectCreateView):
    model = Token
    fields = ("name", "symbol", "blockchain", "last_value")


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
