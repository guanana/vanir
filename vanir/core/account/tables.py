from django_tables2 import Column

from vanir.utils.tables import ObjectTable

from .models import Account


class AccountTable(ObjectTable):
    total_value = Column(
        accessor="total_value_account_table",
        verbose_name="Total Value",
        orderable=False,
    )

    class Meta:
        model = Account
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "exchange", "total_value", "default_fee_rate")
