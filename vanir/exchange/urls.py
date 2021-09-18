from django.urls import path

from .views import ExchangeListView, ExchangeCreateView, ExchangeUpdateView, ExchangeDetailView, ExchangeDeleteView

app_name = "exchange"
urlpatterns = [
        path('', ExchangeListView.as_view(), name="exchange_list"),
        path('add/', ExchangeCreateView.as_view(), name="exchange_add"),
        path('edit/<int:pk>/', ExchangeUpdateView.as_view(), name='exchange_update'),
        path('<int:pk>/', ExchangeDetailView.as_view(), name='exchange_detail'),
        path('delete/<int:pk>/', ExchangeDeleteView.as_view(), name='exchange_delete'),

]
