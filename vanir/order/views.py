from dal import autocomplete
from django.db.models import Q
from django.urls import reverse_lazy

from vanir.utils.views import (
    ObjectCreateView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListFilterView,
)

###
# LimitOrder
###
from ..core.account.models import Account
from ..core.token.models import Token
from .filtersets import (
    LimitOrderFilter,
    MarketOrderFilter,
    StopLossOrTakeProfitLimitOrderFilter,
    StopPriceOrderFilter,
)
from .forms import LimitForm, MarketForm, StopLossOrTakeProfitLimitForm, StopPriceForm
from .models import (
    LimitOrder,
    MarketOrder,
    StopLossOrTakeProfitLimitOrder,
    StopPriceOrder,
)
from .tables import (
    LimitOrderTable,
    MarketOrderTable,
    StopLossOrTakeProfitLimitOrderTable,
    StopPriceOrderTable,
)


class LimitOrderCreateView(ObjectCreateView):
    form_class = LimitForm
    model = LimitOrder
    # TODO: Explore django-autocomplete-light to filter token_from


class LimitOrderListView(ObjectListFilterView):
    model = LimitOrder
    table_class = LimitOrderTable
    filterset_class = LimitOrderFilter


class LimitOrderDetailView(ObjectDetailView):
    model = LimitOrder
    template_name = "order/order_detail.html"
    table_class = LimitOrderTable


class LimitOrderDeleteView(ObjectDeleteView):
    model = LimitOrder
    success_url = reverse_lazy("order:limitorder_list")


###
# MarketOrder
###
class MarketOrderCreateView(ObjectCreateView):
    model = MarketOrder
    form_class = MarketForm


class MarketOrderListView(ObjectListFilterView):
    model = MarketOrder
    table_class = MarketOrderTable
    filterset_class = MarketOrderFilter


class MarketOrderDetailView(ObjectDetailView):
    model = MarketOrder
    table_class = MarketOrderTable
    template_name = "order/order_detail.html"


class MarketOrderDeleteView(ObjectDeleteView):
    model = MarketOrder
    success_url = reverse_lazy("order:marketorder_list")


###
# StopPriceOrder
###
class StopPriceOrderCreateView(ObjectCreateView):
    model = StopPriceOrder
    form_class = StopPriceForm


class StopPriceOrderListView(ObjectListFilterView):
    model = StopPriceOrder
    table_class = StopPriceOrderTable
    filterset_class = StopPriceOrderFilter


class StopPriceOrderDetailView(ObjectDetailView):
    model = StopPriceOrder
    template_name = "order/order_detail.html"
    table_class = StopPriceOrderTable


class StopPriceOrderDeleteView(ObjectDeleteView):
    model = StopPriceOrder
    success_url = reverse_lazy("order:stoppriceorder_list")


###
# StopLossOrTakeProfitLimitOrder
###
class StopLossOrTakeProfitLimitOrderCreateView(ObjectCreateView):
    model = StopLossOrTakeProfitLimitOrder
    form_class = StopLossOrTakeProfitLimitForm


class StopLossOrTakeProfitLimitOrderListView(ObjectListFilterView):
    model = StopLossOrTakeProfitLimitOrder
    table_class = StopLossOrTakeProfitLimitOrderTable
    filterset_class = StopLossOrTakeProfitLimitOrderFilter


class StopLossOrTakeProfitLimitOrderDetailView(ObjectDetailView):
    model = StopLossOrTakeProfitLimitOrder
    template_name = "order/order_detail.html"
    table_class = StopLossOrTakeProfitLimitOrderTable


class StopLossOrTakeProfitLimitOrderDeleteView(ObjectDeleteView):
    model = StopLossOrTakeProfitLimitOrder
    success_url = reverse_lazy("order:stoplossortakeprofitlimitorder_list")


#####
# Autocomplete
#####
class TokenFromAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Token.objects.none()
        account_pk = self.forwarded.get("account", None)
        try:
            qs = Token.objects.filter(accounttokens__account_id=account_pk)
        except ValueError:
            qs = Token.objects.none()
        if self.q:
            qs = qs.filter(Q(symbol__icontains=self.q) | Q(name__icontains=self.q))
        return qs


class TokenToAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Token.objects.none()
        qs = Token.objects.all()
        token_from_pk = self.forwarded.get("token_from", None)
        account_pk = self.forwarded.get("account", None)
        try:
            account = Account.objects.get(pk=account_pk)
            token_from = Token.objects.get(pk=token_from_pk)
        except (Account.DoesNotExist, Token.DoesNotExist):
            return Token.objects.none()
        if token_from and account:
            try:
                allowed = account.exchange_obj.pairs_info[token_from.symbol]
                qs = qs.filter(symbol__in=allowed)
            except KeyError:
                return Token.objects.none()
        else:
            return Token.objects.none()
        return qs
