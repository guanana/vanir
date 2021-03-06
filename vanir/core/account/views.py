from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView

from vanir.core.account.helpers.balance import update_balance
from vanir.core.account.models import Account, AccountTokens
from vanir.core.account.tables import AccountTable
from vanir.core.account.utils import exchange_view_render
from vanir.core.exchange.libs.exchanges import ExtendedExchange
from vanir.core.token.models import Token
from vanir.core.token.tables import AccountTokenTableValue
from vanir.utils.datasource.coingecko import CoinGeckoVanir
from vanir.utils.views import ObjectCreateView, ObjectDeleteView, ObjectListView, ObjectUpdateView


class AccountCreateView(ObjectCreateView):
    model = Account
    fields = (
        "name",
        "exchange",
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
    fields = ("name", "exchange", "api_key", "secret", "default", "token_pair")

    def get_form(self, *args, **kwargs):
        """
        Filter token_pair to only allow fiat and avoid
        user selecting random tokens
        :param args:
        :param kwargs:
        :return: form with new field queryset
        """
        form = super().get_form(*args, **kwargs)
        form.fields["token_pair"].queryset = Token.objects.filter(token_type="FIAT")
        return form


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    table_class = AccountTable
    template_name = "account/account_detail.html"

    def get_context_data(self, **kwargs):
        """
        Add accounttokens table into context so it can
        be displayed
        :return: context
        """
        table = self.table_class(self.model.objects.filter(pk=self.kwargs["pk"]))
        table_accounttokens = AccountTokenTableValue(
            Token.objects.filter(accounttokens__account__pk=self.kwargs["pk"]),
            account_pk=self.kwargs["pk"],
        )
        context = super().get_context_data()
        context["table_account"] = table
        context["table"] = table_accounttokens.paginate(per_page=50)
        return super().get_context_data(**context)


class AccountTokenBulkUpdateValueView(LoginRequiredMixin, DetailView):
    model = Account

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        if self.object.extended_exchange or isinstance(
            self.object.exchange_obj, CoinGeckoVanir
        ):
            update_balance(self.object)
            messages.info(request, "Tokens updated")
        else:
            messages.warning(
                request, "You need to configure a supported exchange for this operation"
            )
        return redirect(
            reverse("account:account_detail", kwargs={"pk": self.object.pk})
        )


class AccountDeleteView(ObjectDeleteView):
    model = Account
    success_url = reverse_lazy("account:account_list")


@login_required
def exchange_testview(request, pk):
    if Account.objects.get(pk=pk).extended_exchange:
        response = Account.objects.get(pk=pk).exchange_obj.test()
        return exchange_view_render("account/account_test.html", response, request)
    else:
        messages.warning(
            request, "You need to configure a supported exchange for this operation"
        )
        return redirect(reverse("account:account_more", kwargs={"pk": pk}))


@login_required
def delete_tokens_account(request, pk):
    Account.objects.get(pk=pk).clear_tokens()
    response = True
    return exchange_view_render("account/account_delete_tokens.html", response, request)


@login_required
def exchange_balanceview(request, pk):
    if Account.objects.get(pk=pk).extended_exchange:
        response = Account.objects.get(pk=pk).exchange_obj.get_balance_html()
        return exchange_view_render(
            "account/account_balance.html",
            response,
            request,
            object=Account.objects.get(pk=pk),
        )
    else:
        messages.warning(
            request, "You need to configure a supported exchange for this operation"
        )
        return redirect(reverse("account:account_more", kwargs={"pk": pk}))


@login_required
def exchange_importtokens(request, pk):
    account = Account.objects.get(pk=pk)
    if account.extended_exchange:
        response = update_balance(account)
        return exchange_view_render("account/account_import.html", response, request)
    return redirect(reverse("account:account_detail", kwargs={"pk": pk}))


class AccountTokensCreateView(ObjectCreateView):
    model = AccountTokens
    fields = ("token", "quantity")

    def form_valid(self, form):
        form.instance.account = Account.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)


class AccountTokensUpdateView(ObjectUpdateView):
    model = AccountTokens
    fields = ("token", "quantity")


class AccountTokensDeleteView(ObjectDeleteView):
    model = AccountTokens
    success_url = reverse_lazy("account:account_list")
