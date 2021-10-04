from vanir.plugins.new_coin_bot.models import BinanceNewToken, NewCoinConfig
from vanir.utils.tables import ObjectTable


class BinanceNewTokenTable(ObjectTable):
    class Meta:
        model = BinanceNewToken
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "name",
            "created_on",
            "updated",
            "symbol",
            "listing_day",
            "discovered_method",
        )
        order_by = "-listing_day"


class NewCoinConfigTable(ObjectTable):
    class Meta:
        model = NewCoinConfig
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "name",
            "created_on",
            "updated",
            "scrapping_interval",
            "activate_scheduler",
            "auto_clean",
        )
