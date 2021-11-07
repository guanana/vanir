import logging
import re
from datetime import datetime
from functools import cache, cached_property

import lxml  # noqa # pylint: disable=unused-impo
import requests
from bs4 import BeautifulSoup
from django.utils import timezone

logger = logging.getLogger(__name__)

requests_session = requests.Session()


class BaseScrap:
    """Base scrap class"""
    def __init__(self):
        self.url = ""
        self.match_lines = dict()

    def _raw_content(self):
        """
        Get web raw content
        :return: soup object with the web data
        :rtype: BeautifulSoup
        """
        page = requests_session.get(self.url, headers={"User-Agent": ""})
        if not page:
            raise ValueError(f"There was a problem with the connection to {self.url}")
        soup = BeautifulSoup(page.content, "lxml")
        return soup


class AnnouncementScrap(BaseScrap):
    """Binance Announcement Scrap Base class"""
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
        :return: list(symbols: str)
        :rtype: list
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
    """Scrap Binance implementation"""
    URL_HREF_PATTERN = re.compile("href=(?P<url>)")  # noqa W605
    CLEAN_WORDS = ["Margin", "Isolated", "Futures"]

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
        """
        Find all links
        :return: List of links
        :rtype: list
        """
        content = self._raw_content().findAll("a", id=self.url_pattern)
        return [item.text for item in content]

    @property
    def url_lines(self):
        """
        Index in a dictionary the urls
        :return: dictionary indexed
        :rtype: dict
        """
        content = self._raw_content().find_all("a", id=self.url_pattern)
        dict_urls = {
            idx: f"{self.base_url}{item['href']}" for idx, item in enumerate(content)
        }
        return dict_urls

    def discard_match(self, line):
        """
        Discard unwanted lines
        :param line: line to check
        :return: If discard True, else False
        :rtype: bool
        """
        match = [
            True for discard_word in self.CLEAN_WORDS if discard_word in line.split()
        ]
        if match:
            return True
        return False

    @cache
    def direct_list_tokens(self):
        """
        Scrapes new listings page for and returns new Symbol when appropriate
        :return: Token in the announcement
        :rtype: list
        """
        direct_list_tokens = []
        for idx, line in enumerate(self.text_content):
            match_pattern = self.LIST_PATTERN.search(line)
            discard = self.discard_match(line)
            if match_pattern and not discard:
                try:
                    symbol = match_pattern.group("symbol")[1:-1]
                    direct_list_tokens.append(symbol)
                    self.match_lines.update({symbol: idx})
                except AttributeError:
                    pass
        return direct_list_tokens

    @cache
    def new_pair_tokens(self):
        """
        Scrapes new pairs and returns new pairs when appropriate
        :return: Pairs in the announcement
        :rtype: list
        """
        new_pair_tokens = []
        for idx, line in enumerate(self.text_content):
            match_pattern = self.PAIR_PATTERN.findall(line)
            discard = self.discard_match(line)
            if match_pattern and not discard:
                for pair in match_pattern:
                    symbol1 = pair.split("/")[0]
                    symbol2 = pair.split("/")[1]
                    new_pair_tokens.append(symbol1)
                    new_pair_tokens.append(symbol2)
                    self.match_lines[symbol1] = idx
                    self.match_lines[symbol2] = idx
        return new_pair_tokens

    @cached_property
    def _last_token_announcements(self):
        """
        Wrapup function to check the tokens and pairs
        :return: list of matching lines
        :rtype: list
        """
        self.direct_list_tokens()
        self.new_pair_tokens()
        return list(self.match_lines.keys())

    @cache
    def release_date(self, line):
        """
        Check for release date from the announcement
        :param line: Line to check
        :return: date of the announcement
        :rtype datetime
        """
        scrap_timestamp_obj = ScrapTimestamp()
        if len(self._last_token_announcements) > 0:
            try:
                url = self.url_lines[line]
                scrap_timestamp_obj.url = url
                token_date = scrap_timestamp_obj.get_date(line)
                return token_date
            except KeyError:
                logger.error("Problem finding the match line")


class ScrapTimestamp(BaseScrap):
    match_lines = list()
    year_pattern = "(?P<year>(19|20)\d{2})"  # noqa W605
    month_pattern = "(?P<month>0[1-9]|1[0-2])"
    day_pattern = "(?P<day>0[1-9]|[12][0-9]|3[01])"
    hour_pattern = "(?P<hour>[0-1][0-9]|2[0-4])"
    minute_pattern = "(?P<minute>[0-5][0-9])"
    timezone_pattern = "(?P<timezone>\(UTC\))"  # noqa W605
    am_pm_pattern = "(?P<am_pm_utc>AM|PM)"
    TIMESTAMP_PATTERN_BASIC = (
        f"{year_pattern}-"
        f"{month_pattern}-"
        f"{day_pattern}.+"
        f"{hour_pattern}:"
        f"{minute_pattern}\s"
    )

    TIMESTAMP_PATTERN_24H = re.compile(
        f"(.*(?P<all>{TIMESTAMP_PATTERN_BASIC}{timezone_pattern}))"
    )  # noqa W605
    TIMESTAMP_PATTERN_AM_PM = re.compile(
        f"(.*(?P<all>{TIMESTAMP_PATTERN_BASIC}{am_pm_pattern}\s{timezone_pattern}))"
    )  # noqa W605

    def get_date(self, line):
        """
        Get date of the announcement with regexp
        :param line: Line to check
        :return: date or none
        :rtype: datetime or None
        """
        try:
            return self.match_lines[line]
        except KeyError:
            pass
        date = None
        article_content = self._raw_content().find_all("article")
        try:
            content_24h = re.match(self.TIMESTAMP_PATTERN_24H, article_content[0].text)
            content_am_pm = re.match(
                self.TIMESTAMP_PATTERN_AM_PM, article_content[0].text
            )
        except IndexError:
            logger.error(f"No article tag found for {self.url}")
            return
        if not content_24h and not content_am_pm:
            logger.error(f"No date found for {self.url}")
            return
        if content_24h:
            try:
                date = datetime.strptime(
                    content_24h.group("all"), "%Y-%m-%d %H:%M (%Z)"
                )
                current_tz = timezone.utc
                date = current_tz.localize(date)
            except ValueError:
                logger.error(
                    f'Something happened wit this time import {content_24h.group("all")}'
                )
        else:
            try:
                date = datetime.strptime(
                    content_am_pm.group("all"), "%Y-%m-%d %I:%M %p (%Z)"
                )
                current_tz = timezone.utc
                date = current_tz.localize(date)
            except ValueError:
                logger.error(
                    f'Something happened with this time import {content_am_pm.group("all")}'
                )
        self.match_lines[line] = date
        return date

    def get_news_publish_date(self):
        """
        Get the date of the announcement (not the date of listing)
        :return: date of announcement
        :rtype: datetime or None
        """
        news_publish = self._raw_content().find("div", {"class": "css-17s7mnd"})
        try:
            date = datetime.strptime(news_publish.text, "%Y-%m-%d %H:%M")
        except ValueError:
            logger.error(f"Something happened with this time import {news_publish}")
            return
        return date
