from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy

from vanir.account.models import Account
from vanir.account.tables import AccountTable
from vanir.exchange.utils import SUPPORTED_EXCHANGES
from vanir.utils.helpers import get_nav_menu
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
        "exchange",
        "user",
        "api_key",
        "secret",
        "tld",
        "password",
        "default_fee_rate",
    )


class AccountListView(ObjectListView):
    model = Account
    table_class = AccountTable


class AccountUpdateView(ObjectUpdateView):
    model = Account


class AccountDetailView(ObjectDetailView):
    model = Account


class AccountDeleteView(ObjectDeleteView):
    model = Account
    success_url = reverse_lazy("account:account_list")


def exchangetestview(request, pk):
    account = Account.objects.get(pk=pk)
    classname = SUPPORTED_EXCHANGES[account.exchange.name]
    exchange_obj = classname(account)
    response = exchange_obj.test()
    template = loader.get_template("account/account_test.html")
    context = {
        "con": response,
    }
    context = get_nav_menu(context)
    return HttpResponse(template.render(context, request))


def exchangebalanceview(request, pk):
    account = Account.objects.get(pk=pk)
    classname = SUPPORTED_EXCHANGES[account.exchange.name]
    exchange_obj = classname(account)
    response = exchange_obj.get_balance()
    template = loader.get_template("account/account_balance.html")
    context = {
        "con": response,
    }
    context = get_nav_menu(context)
    return HttpResponse(template.render(context, request))
