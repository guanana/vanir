from django.urls import path

from . import views

app_name = "order"
urlpatterns = [
    # STOP PRICE ORDER
    path(
        "stoppriceorder/",
        views.StopPriceOrderListView.as_view(),
        name="stoppriceorder_list",
    ),
    path(
        "stoppriceorder/add/",
        views.StopPriceOrderCreateView.as_view(),
        name="stoppriceorder_add",
    ),
    path(
        "stoppriceorder/<int:pk>/",
        views.StopPriceOrderDetailView.as_view(),
        name="stoppriceorder_detail",
    ),
    path(
        "stoppriceorder/<int:pk>/delete/",
        views.StopPriceOrderDeleteView.as_view(),
        name="stoppriceorder_delete",
    ),
    # STOPLOSS OR TAKEPROFIT LIMIT ORDER
    path(
        "stoplossortakeprofitorderlimit/",
        views.StopLossOrTakeProfitLimitOrderListView.as_view(),
        name="stoplossortakeprofitlimitorder_list",
    ),
    path(
        "stoplossortakeprofitorderlimit/add/",
        views.StopLossOrTakeProfitLimitOrderCreateView.as_view(),
        name="stoplossortakeprofitlimitorder_add",
    ),
    path(
        "stoplossortakeprofitorderlimit/<int:pk>/",
        views.StopLossOrTakeProfitLimitOrderDetailView.as_view(),
        name="stoplossortakeprofitlimitorder_detail",
    ),
    path(
        "stoplossortakeprofitorderlimit/<int:pk>/delete/",
        views.StopLossOrTakeProfitLimitOrderDeleteView.as_view(),
        name="stoplossortakeprofitlimitorder_delete",
    ),
    # LIMIT ORDER
    path("limitorder/", views.LimitOrderListView.as_view(), name="limitorder_list"),
    path(
        "limitorder/add/", views.LimitOrderCreateView.as_view(), name="limitorder_add"
    ),
    path(
        "limitorder/<int:pk>/",
        views.LimitOrderDetailView.as_view(),
        name="limitorder_detail",
    ),
    path(
        "limitorder/<int:pk>/delete/",
        views.LimitOrderDeleteView.as_view(),
        name="limitorder_delete",
    ),
    # MARKET
    path("marketorder/", views.MarketOrderListView.as_view(), name="marketorder_list"),
    path(
        "marketorder/add/",
        views.MarketOrderCreateView.as_view(),
        name="marketorder_add",
    ),
    path(
        "marketorder/<int:pk>/",
        views.MarketOrderDetailView.as_view(),
        name="marketorder_detail",
    ),
    path(
        "marketorder/<int:pk>/delete/",
        views.MarketOrderDeleteView.as_view(),
        name="marketorder_delete",
    ),
    path(
        "tokento-autocomplete/",
        views.TokenToAutocomplete.as_view(),
        name="tokento_autocomplete",
    ),
    path(
        "tokenfrom-autocomplete/",
        views.TokenFromAutocomplete.as_view(),
        name="tokenfrom_autocomplete",
    ),
    path(
        "price-autocomplete/",
        views.TokenPriceAutocomplete,
        name="price_autocomplete",
    ),
]
