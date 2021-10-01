from vanir.plugins.new_coin_bot.scrappers import AnnouncementScrapModel, ScrapBinance

from .choices import DiscoverMethod
from .helpers import token_already_exists
from .models import BinanceNewTokenModel


class ScrapBinanceModel(ScrapBinance, AnnouncementScrapModel):
    DISCOVER_METHOD = DiscoverMethod.BINANCE_SCRAPPER

    def remove_existing_tokens(self):
        for token_symbol in self._last_token_announcements:
            if token_already_exists(token_symbol):
                self._last_token_announcements.pop()

    def import_token_announcements(self):
        self.remove_existing_tokens()
        for token_symbol in self._last_token_announcements:
            new_coin = BinanceNewTokenModel.objects.get_or_create(
                name=token_symbol,
                symbol=token_symbol,
                discovered_method=self.DISCOVER_METHOD,
            )
            new_coin.increase_announcement_seen()
