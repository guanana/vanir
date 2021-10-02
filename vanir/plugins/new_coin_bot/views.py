from vanir.plugins.new_coin_bot.models import BinanceNewToken
from vanir.plugins.new_coin_bot.tables import BinanceNewTokenTable
from vanir.plugins.views import PluginListView


class BinanceNewTokenListView(PluginListView):
    model = BinanceNewToken
    table_class = BinanceNewTokenTable
