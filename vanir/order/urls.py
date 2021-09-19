from django.urls import path

from .views import OrderListView, OrderCreateView, OrderDetailView

app_name = "order"
urlpatterns = [
        path('', OrderListView.as_view(), name="order_list"),
        path('add/', OrderCreateView.as_view(), name="order_add"),
        path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
        # path('<int:pk>/edit/', BlockchainUpdateView.as_view(), name='blockchain_update'),
        # path('<int:pk>/delete/', BlockchainDeleteView.as_view(), name='blockchain_delete'),

]
