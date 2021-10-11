from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView

from vanir.core.account.helpers.balance import update_balance
from vanir.core.account.models import Account
from vanir.core.account.tables import AccountTable
from vanir.core.account.utils import exchange_view_render
from vanir.core.exchange.libs.exchanges import ExtendedExchange
from vanir.core.token.helpers.import_utils import qs_update
from vanir.core.token.models import Token
from vanir.core.token.tables import TokenTableValue
from vanir.utils.views import (
    ObjectCreateView,
    ObjectDeleteView,
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
    fields = (
        "name",
        "exchange",
        "user",
        "api_key",
        "secret",
        "tld",
        "testnet",
        "default",
    )


class AccountDetailView(DetailView):
    model = Account
    table_class = AccountTable
    template_name = "account/account_detail.html"

    def get_context_data(self, **kwargs):
        table = self.table_class(self.model.objects.filter(pk=self.kwargs["pk"]))
        table_accounttokens = TokenTableValue(
            Token.objects.filter(accounttokens__account__pk=self.kwargs["pk"]),
            account_pk=self.kwargs["pk"],
        )
        context = super().get_context_data()
        context["table_account"] = table
        context["table"] = table_accounttokens
        return super().get_context_data(**context)


class AccountTokenBulkUpdateValueView(DetailView):
    model = Account

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        update_balance(self.object)
        token_subset = self.object.accounttokens_set
        qs_update(token_subset.all(), self.object)
        messages.info(request, "Tokens updated")
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
    response = update_balance(account)
    return exchange_view_render("account/account_import.html", response, request)
