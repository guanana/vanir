from django.urls import reverse_lazy

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
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class TokenBulkUpdateValueView(ObjectListView):
    model = Token
    table_class = TokenTable

    def get(self, request, *args, **kwargs):
        bulk_update(Token.objects.all())
        return super(TokenBulkUpdateValueView, self).get(request, *args, **kwargs)
