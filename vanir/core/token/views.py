from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from vanir.core.token.filtersets import TokenFilter
from vanir.core.token.helpers.import_utils import bulk_update
from vanir.core.token.models import Token
from vanir.core.token.tables import TokenTable
from vanir.utils.exceptions import AccountRequiredError, ExchangeExtendedFunctionalityError
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
    fields = ("name", "symbol", "last_value", "token_type")


class TokenListView(ObjectListFilterView):
    model = Token
    table_class = TokenTable
    filterset_class = TokenFilter


class TokenUpdateView(ObjectUpdateView):
    model = Token


class TokenDetailView(ObjectDetailView):
    model = Token
    table_class = TokenTable
    template_name = "token/token_detail.html"


class TokenDeleteView(ObjectDeleteView):
    model = Token
    success_url = reverse_lazy("token:token_list")


class TokenDetailUpdateValueView(ObjectDetailView):
    model = Token
    table_class = TokenTable

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if not self.object.set_value():
            messages.info(
                message="Last value not updated, you can update it manually",
                request=request,
            )
        else:
            messages.success(message="Last value updated correctly", request=request)
        return redirect(reverse("token:token_detail", kwargs={"pk": self.object.pk}))


class TokenBulkUpdateValueView(ObjectListView):
    model = Token
    table_class = TokenTable

    def get(self, request, *args, **kwargs):
        try:
            bulk_update()
        except AccountRequiredError:
            messages.error(
                request,
                "You need to have a supported exchange account configured as default",
            )
            return redirect(reverse("token:token_list"))
        except ExchangeExtendedFunctionalityError:
            messages.warning(
                request, "You need to configure a supported exchange for this operation"
            )
            return redirect(reverse("token:token_list"))
        messages.info(request, "Bulk update completed")
        return redirect(reverse("token:token_list"))
