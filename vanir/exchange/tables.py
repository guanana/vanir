from .models import Exchange
from vanir.utils.tables import ObjectTable


class ExchangeTable(ObjectTable):
    class Meta:
        model = Exchange
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "default_fee", "native_token")
