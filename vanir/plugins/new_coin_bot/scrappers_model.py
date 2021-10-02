from vanir.plugins.new_coin_bot.scrappers import ScrapBinance

from .choices import DiscoverMethod
from .helpers import token_already_exists
from .models import BinanceNewToken


class ScrapBinanceModel(ScrapBinance):
    DISCOVER_METHOD = DiscoverMethod.BINANCE_SCRAPPER

    def _clean(self):
        self._remove_existing_tokens()

    def _remove_existing_tokens(self):
        for token_symbol in self._last_token_announcements:
            if token_already_exists(token_symbol):
                self._last_token_announcements.pop()

    def import_token_announcements(self):
        self._clean()
        for token_symbol in self._last_token_announcements:
            new_coin = BinanceNewToken.objects.get_or_create(
                name=token_symbol,
                symbol=token_symbol,
                discovered_method=self.DISCOVER_METHOD,
                listing_day=self.release_date(token_symbol),
            )
            new_coin.increase_announcement_seen()
