import django_tables2 as tables
from .models import Token
from vanir.utils.tables import ObjectTable


class TokenTable(ObjectTable):
    class Meta:
        model = Token
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "symbol", "blockchain", "decimals")
