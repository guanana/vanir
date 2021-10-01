import re

import requests
from bs4 import BeautifulSoup

# from .choices import DiscoverMethod
# from .helpers import token_already_exists
# from .models import BinanceNewTokenModel


class BaseScrap:
    def __init__(self, scrap_option: str):
        self.scrap_option = scrap_option
        self.url = ""
        self.match_lines = dict()

    def _raw_content(self):
        page = requests.get(self.url)
        if not page:
            raise ValueError(f"There was a problem with the connection to {self.url}")
        soup = BeautifulSoup(page.content, "html.parser")
        return soup


class AnnouncementScrap(BaseScrap):
    LIST_PATTERN = re.compile("List .* (?P<symbol>\((\w+\)))")  # noqa W605
    PAIR_PATTERN = re.compile("(?P<pair>\w+/\w+)")  # noqa W605
    ANNOUNCEMENT_SCRAP_URLS = {
        "Binance": {
            "base_url": "https://www.binance.com",
            "announcement_path": "/en/support/announcement/c-48",
            "scrap_pattern": re.compile("link-0-"),
        }
    }

    @property
    def _last_token_announcements(self):
        """
        Aggregation method that will join all list of tokens and return just
        a unique list of tokens to import
        @returns: list(symbols: str)
        """
        raise NotImplementedError


class AnnouncementScrapModel(BaseScrap):
    def remove_existing_tokens(self):
        """
        Checks against existing tokens in core Token DB and remove
        from the list the ones are already present
        """
        raise NotImplementedError

    def import_token_announcements(self):
        """
        Add into model the tokens that are really new
        """
        raise NotImplementedError


class ScrapBinance(AnnouncementScrap):
    URL_HREF_PATTERN = re.compile("href=(?P<url>)")  # noqa W605

    def __init__(self, scrap_option: str = "Binance"):
        super().__init__(scrap_option)

        self.base_url = self.ANNOUNCEMENT_SCRAP_URLS.get(self.scrap_option)["base_url"]
        self.url = f'{self.base_url}{self.ANNOUNCEMENT_SCRAP_URLS.get(self.scrap_option)["announcement_path"]}'
        self.url_pattern = self.ANNOUNCEMENT_SCRAP_URLS.get(self.scrap_option)[
            "scrap_pattern"
        ]
        if not self.url:
            raise ValueError(f"{self.scrap_option} not a valid option")
        self.link_content = {}

    @property
    def text_content(self):
        content = self._raw_content().findAll("a", id=self.url_pattern)
        return [item.text for item in content]

    @property
    def url_lines(self):
        content = self._raw_content().find_all("a", id=self.url_pattern)
        dict_urls = {
            idx: f"{self.base_url}{item['href']}" for idx, item in enumerate(content)
        }
        return dict_urls

    @property
    def direct_list_tokens(self):
        """
        Scrapes new listings page for and returns new Symbol when appropriate
        """
        direct_list_tokens = []
        for idx, line in enumerate(self.text_content):
            match_pattern = self.LIST_PATTERN.search(line)
            if match_pattern:
                try:
                    symbol = match_pattern.group("symbol")[1:-1]
                    direct_list_tokens.append(symbol)
                    self.match_lines.update({symbol: idx})
                except AttributeError:
                    pass
        return direct_list_tokens

    @property
    def new_pair_tokens(self):
        """
        Scrapes new pairs and returns new pairs when appropriate
        """
        new_pair_tokens = []
        for idx, line in enumerate(self.text_content):
            match_pattern = self.PAIR_PATTERN.findall(line)
            if match_pattern:
                for pair in match_pattern:
                    symbol1 = pair.split("/")[0]
                    symbol2 = pair.split("/")[1]
                    new_pair_tokens.append(symbol1)
                    new_pair_tokens.append(symbol2)
                    self.match_lines[symbol1] = idx
                    self.match_lines[symbol2] = idx
        return new_pair_tokens

    @property
    def _last_token_announcements(self):
        return self.direct_list_tokens + self.new_pair_tokens

    def follow_urls(self, symbol):
        if len(self._last_token_announcements) > 0:
            try:
                return self.url_lines[self.match_lines[symbol]]
            except KeyError:
                pass
