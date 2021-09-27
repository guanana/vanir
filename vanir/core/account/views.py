from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from vanir.core.account.models import Account
from vanir.core.account.tables import AccountTable
from vanir.core.account.utils import exchange_view_render
from vanir.core.exchange.libs.exchanges import ExtendedExchange
from vanir.core.token.helpers.import_utils import bulk_update, qs_update, token_import
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


class AccountTokenBulkUpdateValueView(ObjectDetailView):
    model = Account

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        token_subset = self.object.accounttokens_set
        messages.info(request, "Tokens updated")
        qs_update(token_subset.all(), self.object)
        return redirect(
            reverse("account:account_detail", kwargs={"pk": self.object.pk})
        )


class AccountDeleteView(ObjectDeleteView):
    model = Account
    success_url = reverse_lazy("account:account_list")


def exchange_testview(request, pk):
    response = Account.objects.get(pk=pk).exchange_obj.test()
    return exchange_view_render("account/account_test.html", response, request)


def delete_tokens_account(request, pk):
    Account.objects.get(pk=pk).clear_tokens()
    response = True
    return exchange_view_render("account/account_delete_tokens.html", response, request)


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
    df = account.exchange_obj.get_balance()
    response = []
    for index, row in df.iterrows():
        token_import(
            account=account,
            token_symbol=row["asset"],
            quantity=float(row["free"]) + float(row["locked"]),
        )
        response.append(row["asset"])
    bulk_update()
    return exchange_view_render("account/account_import.html", response, request)
