import django_tables2 as tables
from .models import Token


class TokenTable(tables.Table):
    class Meta:
        model = Token
        template_name = "django_tables2/bootstrap.html"

