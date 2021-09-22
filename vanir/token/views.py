from django.urls import reverse_lazy

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
        self.object = self.get_object()
        self.object.get_value()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class TokenBulkUpdateValueView(ObjectListView):
    model = Token
    table_class = TokenTable

    def get(self, request, *args, **kwargs):
        for token in Token.objects.all():
            try:
                token.get_value()
            except ValueError:
                pass
        return super(TokenBulkUpdateValueView, self).get(request, *args, **kwargs)
