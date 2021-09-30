from django.db import models

from vanir.core.token.models import Token
from vanir.plugins.models import PluginBase
from vanir.plugins.new_coin_bot.choices import DiscoverMethod


class NewCoinModel(Token, PluginBase):
    discovered_method = models.CharField(max_length=25, choices=DiscoverMethod.choices)
    listing_day = models.DateTimeField()
