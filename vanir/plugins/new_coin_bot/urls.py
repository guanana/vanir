from django.urls import path

from .views import (
    BinanceNewTokenCreateView,
    BinanceNewTokenDeleteView,
    BinanceNewTokenDetailView,
    BinanceNewTokenListView,
    BinanceNewTokenPromoteView,
    BinanceNewTokenUpdateValueView,
    BinanceNewTokenUpdateView,
    NewCoinConfigCreateView,
    NewCoinConfigDeleteView,
    NewCoinConfigDetailView,
    NewCoinConfigListView,
    NewCoinConfigUpdateView,
)

app_name = "new_coin_bot"


urlpatterns = [
    # New Coin Config
    path("config/", NewCoinConfigListView.as_view(), name="newcoinconfig_list"),
    path("config/add/", NewCoinConfigCreateView.as_view(), name="newcoinconfig_add"),
    path(
        "config/<int:pk>/",
        NewCoinConfigDetailView.as_view(),
        name="newcoinconfig_detail",
    ),
    path(
        "config/<int:pk>/edit/",
        NewCoinConfigUpdateView.as_view(),
        name="newcoinconfig_edit",
    ),
    path(
        "config/<int:pk>/delete/",
        NewCoinConfigDeleteView.as_view(),
        name="newcoinconfig_delete",
    ),
    # Binance New Token
    path(
        "binancenewtoken/",
        BinanceNewTokenListView.as_view(),
        name="binancenewtoken_list",
    ),
    path(
        "binancenewtoken/add/",
        BinanceNewTokenCreateView.as_view(),
        name="binancenewtoken_add",
    ),
    path(
        "binancenewtoken/<int:pk>/",
        BinanceNewTokenDetailView.as_view(),
        name="binancenewtoken_detail",
    ),
    path(
        "binancenewtoken/<int:pk>/edit/",
        BinanceNewTokenUpdateView.as_view(),
        name="binancenewtoken_edit",
    ),
    path(
        "binancenewtoken/<int:pk>/delete/",
        BinanceNewTokenDeleteView.as_view(),
        name="binancenewtoken_delete",
    ),
    path(
        "binancenewtoken/update/",
        BinanceNewTokenUpdateValueView.as_view(),
        name="binancenewtoken_update",
    ),
    path(
        "binancenewtoken/<int:pk>/promote/",
        BinanceNewTokenPromoteView.as_view(),
        name="binancenewtoken_promote",
    ),
]
