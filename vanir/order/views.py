from vanir.utils.views import ObjectListView, ObjectCreateView, ObjectDetailView
from .models import Order
from .tables import OrderTable


class OrderCreateView(ObjectCreateView):
    model = Order
    fields = ("account", "token_from", "token_to", "side", "orderType", "quoteOrderQty")


class OrderListView(ObjectListView):
    model = Order
    table_class = OrderTable

class OrderDetailView(ObjectDetailView):
    model = Order
