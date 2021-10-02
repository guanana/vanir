from django.urls import path

from .views import BinanceNewTokenListView

app_name = "new_coin_bot"

urlpatterns = [
    path(
        "binancenewtoken/",
        BinanceNewTokenListView.as_view(),
        name="binancenewtoken_list",
    ),
    path(
        "binancenewtoken/",
        BinanceNewTokenListView.as_view(),
        name="binancenewtoken_add",
    ),
]
