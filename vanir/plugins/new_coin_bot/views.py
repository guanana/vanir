from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from vanir.plugins.new_coin_bot.helpers import run_scrap
from vanir.plugins.new_coin_bot.models import BinanceNewToken, NewCoinConfig
from vanir.plugins.new_coin_bot.tables import BinanceNewTokenTable, NewCoinConfigTable
from vanir.plugins.views import (
    PluginCreateView,
    PluginDeleteView,
    PluginDetailView,
    PluginListView,
    PluginUpdateView,
)


# New Coin Config
class NewCoinConfigCreateView(PluginCreateView):
    model = NewCoinConfig
    fields = (
        "scrapper_class_name",
        "scrapping_interval",
        "activate_scheduler",
        "auto_clean",
    )


class NewCoinConfigListView(PluginListView):
    model = NewCoinConfig
    table_class = NewCoinConfigTable


class NewCoinConfigUpdateView(PluginUpdateView):
    model = NewCoinConfig
    fields = ("scrapping_interval", "activate_scheduler", "auto_clean")


class NewCoinConfigDetailView(PluginDetailView):
    model = NewCoinConfig


class NewCoinConfigDeleteView(PluginDeleteView):
    model = NewCoinConfig
    success_url = reverse_lazy("plugins:new_coin_bot:newcoinconfig_list")


# Binance New Token
class BinanceNewTokenCreateView(PluginCreateView):
    model = BinanceNewToken
    fields = ("name", "symbol", "discovered_method", "listing_day")


class BinanceNewTokenListView(PluginListView):
    model = BinanceNewToken
    table_class = BinanceNewTokenTable


class BinanceNewTokenUpdateView(PluginUpdateView):
    model = BinanceNewToken
    fields = (
        "name",
        "discovered_method",
        "listing_day",
    )


class BinanceNewTokenDetailView(PluginDetailView):
    model = BinanceNewToken


class BinanceNewTokenDeleteView(PluginDeleteView):
    model = BinanceNewToken
    success_url = reverse_lazy("plugins:new_coin_bot:binancenewtoken_list")


class BinanceNewTokenUpdateValueView(PluginListView, SuccessMessageMixin):
    model = BinanceNewToken
    table_class = BinanceNewTokenTable
    success_message = "Scrap completed"

    def get(self, request, *args, **kwargs):
        run_scrap()
        return redirect(reverse("plugins:new_coin_bot:binancenewtoken_list"))


class BinanceNewTokenPromoteView(PluginDetailView):
    model = BinanceNewToken

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        token = self.object.promote_to_standard_token()
        return redirect(reverse("token:token_detail", kwargs={"pk": token.pk}))
