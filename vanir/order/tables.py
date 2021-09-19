from .models import Order
from vanir.utils.tables import ObjectTable


class OrderTable(ObjectTable):
    class Meta:
        model = Order
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "account", "token_from", "token_to", "side", "orderType", "quoteOrderQty")
