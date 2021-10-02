from vanir.plugins.new_coin_bot.models import BinanceNewToken
from vanir.utils.tables import ObjectTable


class BinanceNewTokenTable(ObjectTable):
    class Meta:
        model = BinanceNewToken
        template_name = "django_tables2/bootstrap.html"
