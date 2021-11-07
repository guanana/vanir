from django.urls import reverse
from django.utils.html import format_html
from django_tables2 import Column

from vanir.utils.tables import ObjectTable

from ..account.models import AccountTokens
from .models import Token


class TokenTable(ObjectTable):
    def render_last_value(self, value):
        if value == 0:
            return "Pair not supported"
        else:
            return value

    class Meta:
        model = Token
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "symbol", "last_value")


class AccountTokenTableValue(TokenTable):
    def __init__(self, data, account_pk):
        self.account_pk = account_pk
        super().__init__(data)

    name = Column(empty_values=())
    quantity = Column(empty_values=())
    total_value = Column(empty_values=())

    def render_name(self, record):
        accounttoken_pk = AccountTokens.objects.get(
            account__pk=self.account_pk, token__pk=record.pk
        ).pk
        name = Token.objects.get(pk=record.pk).name
        url = reverse("account:account_tokens_edit", kwargs={"pk": accounttoken_pk})
        return format_html(f"<a href={url}>{name}</a>")

    def render_quantity(self, record):
        return AccountTokens.objects.get(
            account__pk=self.account_pk, token__pk=record.pk
        ).quantity

    def render_total_value(self, record):
        return round(
            AccountTokens.objects.get(
                account__pk=self.account_pk, token__pk=record.pk
            ).quantity
            * record.last_value,
            4,
        )

    class Meta:
        sequence = ("name", "symbol", "last_value", "quantity", "total_value")
