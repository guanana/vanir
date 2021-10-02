from django.db import models

from vanir.core.token.models import Coin, Token
from vanir.plugins.models import PluginBase
from vanir.plugins.new_coin_bot.choices import DiscoverMethod, ScheduleScrap
from vanir.utils.models import TimeStampedMixin


class NewCoinConfig(PluginBase, TimeStampedMixin):
    scrapping_interval = models.IntegerField(choices=ScheduleScrap.choices, default=10)


class NewCoin(PluginBase, Coin, TimeStampedMixin):
    discovered_method = models.CharField(max_length=25, choices=DiscoverMethod.choices)
    listing_day = models.DateTimeField(null=True)
    announcement_seen = models.IntegerField(null=True)

    class Meta:
        abstract = True
        unique_together = ("name", "symbol")

    def increase_announcement_seen(self):
        self.announcement_seen += 1
        self.save()

    @property
    def is_new(self):
        if self.announcement_seen <= 1:
            return True
        return False

    def promote_to_standard_token(self):
        """
        Creates a token in the core DB and removes itself from the NewCoinModel
        """
        Token.objects.create(name=self.name, symbol=self.symbol)
        self.delete()


class BinanceNewToken(NewCoin):
    discovered_method = models.CharField(
        max_length=25, choices=DiscoverMethod.choices, default="Binance Scrapper"
    )
