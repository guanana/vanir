from django_tables2 import Column

from vanir.utils.tables import ObjectTable

from ..utils.helpers import fetch_default_account
from .models import Token


class TokenTable(ObjectTable):
    if fetch_default_account():
        last_value = Column(
            verbose_name=f"Last value in {fetch_default_account().token_pair}"
        )

    class Meta:
        model = Token
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "symbol", "blockchain", "last_value")
