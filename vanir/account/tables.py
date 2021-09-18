import django_tables2 as tables
from .models import Account, Exchange


class AccountTable(tables.Table):
    class Meta:
        model = Account
        template_name = "django_tables2/bootstrap.html"
        fields = ("exchange", "user", "tld", "default_fee_rate")

