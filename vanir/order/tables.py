from django_tables2 import tables
from .models import Order

# Orders are not allowed to be edited (at least for now, that's why not inheriting from utils like rest of obj


class OrderTable(tables.Table):
    class Meta:
        model = Order
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "account", "token_from", "token_to", "side", "orderType", "quoteOrderQty")
