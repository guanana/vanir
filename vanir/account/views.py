from django.urls import reverse_lazy

from vanir.account.models import Account
from vanir.account.tables import AccountTable
from vanir.account.utils import exchange_view_render
from vanir.exchange.helpers.main import ExtendedExchange
from vanir.token.helpers.import_utils import token_import
from vanir.utils.views import (
    ObjectCreateView,
    ObjectDeleteView,
    ObjectDetailView,
    ObjectListView,
    ObjectUpdateView,
)


class AccountCreateView(ObjectCreateView):
    model = Account
    fields = (
        "name",
        "exchange",
        "user",
        "api_key",
        "secret",
        "tld",
        "default_fee_rate",
        "token_pair",
        "default",
        "testnet",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["SUPPORTED_EXCHANGES"] = ExtendedExchange.all_supported()
        return context


class AccountListView(ObjectListView):
    model = Account
    table_class = AccountTable


class AccountUpdateView(ObjectUpdateView):
    model = Account
    # TODO: Fix selection of tokens


class AccountDetailView(ObjectDetailView):
    model = Account


class AccountDeleteView(ObjectDeleteView):
    model = Account
    success_url = reverse_lazy("account:account_list")


def exchange_testview(request, pk):
    response = Account.objects.get(pk=pk).exchange_obj.test()
    return exchange_view_render("account/account_test.html", response, request)


def exchange_balanceview(request, pk):
    response = Account.objects.get(pk=pk).exchange_obj.get_balance_html()
    return exchange_view_render(
        "account/account_balance.html",
        response,
        request,
        object=Account.objects.get(pk=pk),
    )


def exchange_importtokens(request, pk):
    account = Account.objects.get(pk=pk)
    exchange_obj = account.exchange_obj
    df = exchange_obj.get_balance()
    response = []
    for index, row in df.iterrows():
        token_import(account, row["asset"], float(row["free"]) + float(row["locked"]))
        response.append(row["asset"])
    return exchange_view_render("account/account_import.html", response, request)
