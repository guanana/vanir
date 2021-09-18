from django.urls import reverse_lazy

from vanir.account.models import Account
from vanir.account.tables import AccountTable
from vanir.utils.views import ObjectListView, ObjectUpdateView, ObjectDetailView, ObjectDeleteView, ObjectCreateView


class AccountCreateView(ObjectCreateView):
    model = Account
    fields = ("exchange", "user", "api_key", "secret", "tld", "password", "default_fee_rate")


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
