import logging
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class BaseScrap:
    def __init__(self):
        self.url = ""
        self.match_lines = dict()

    def _raw_content(self):
        page = requests.get(self.url)
        if not page:
            raise ValueError(f"There was a problem with the connection to {self.url}")
        soup = BeautifulSoup(page.content, "html.parser")
        return soup


class AnnouncementScrap(BaseScrap):
    def __init__(self, scrap_option: str):
        super().__init__()
        self.scrap_option = scrap_option

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

    def release_date(self, symbol):
        scrap_timestamp_obj = ScrapTimestamp()
        if len(self._last_token_announcements) > 0:
            try:
                url = self.url_lines[self.match_lines[symbol]]
                scrap_timestamp_obj.url = url
                token_date = scrap_timestamp_obj.timestamp_content
                return token_date
            except KeyError:
                logger.error("Problem finding the match line")


class ScrapTimestamp(BaseScrap):
    """
    TIMESTAMP_PATTERN = re.compile("(?P<year>^(19|20)\d{2})-"
                                   "(?P<month>0[1-9]|1[0-2])-"
                                   "(?P<day>0[1-9]|[12][0-9]|3[01]).+"
                                   "(?P<hour>[0-1][0-9]|2[0-4]):"
                                   "(?P<minute>[0-5][0-9]).+\((?P<timezone>\w+)\)")
    """

    TIMESTAMP_PATTERN = re.compile(
        ".*(?P<year>(19|20)\d{2})-"
        "(?P<month>0[1-9]|1[0-2])-"
        "(?P<day>0[1-9]|[12][0-9]|3[01]).+"
        "(?P<hour>[0-1][0-9]|2[0-4]):(?P<minute>[0-5][0-9])\s"
        "((AM|PM\s \(UTC\))|\(UTC\))"
    )  # noqa W605

    def find_first_timestamp(self):
        pass

    @property
    def timestamp_content(self):
        article_content = self._raw_content().find_all("article")
        try:
            content = re.match(self.TIMESTAMP_PATTERN, article_content[0].text)
        except IndexError:
            logger.error(f"No article tag found for {self.url}")
            return
        if not content:
            logger.error(f"No date found for {self.url}")
            return

        temp_dict = content.groupdict()
        date_dict = {name: int(value) for name, value in temp_dict.items()}
        date = datetime(**date_dict)
        return date
