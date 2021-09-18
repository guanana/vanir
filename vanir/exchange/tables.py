import django_tables2 as tables
from .models import Exchange


class ExchangeTable(tables.Table):
    class Meta:
        model = Exchange
        template_name = "django_tables2/bootstrap.html"

