from .models import Account, Exchange
from vanir.utils.tables import ObjectTable


class AccountTable(ObjectTable):
    class Meta:
        model = Account
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "exchange", "user", "tld", "default_fee_rate")

