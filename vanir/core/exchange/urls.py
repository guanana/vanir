from django.urls import path

from .views import ExchangeCreateView, ExchangeDeleteView, ExchangeDetailView, ExchangeListView, ExchangeUpdateView

app_name = "exchange"
urlpatterns = [
    path("", ExchangeListView.as_view(), name="exchange_list"),
    path("add/", ExchangeCreateView.as_view(), name="exchange_add"),
    path("<int:pk>/", ExchangeDetailView.as_view(), name="exchange_detail"),
    path("<int:pk>/edit/", ExchangeUpdateView.as_view(), name="exchange_edit"),
    path("<int:pk>/delete/", ExchangeDeleteView.as_view(), name="exchange_delete"),
]
