import re

import requests
from bs4 import BeautifulSoup


class BaseScrap:
    SCRAP_URLS = {
        "Binance": {
            "base_url": "https://www.binance.com",
            "announcement_path": "/en/support/announcement/c-48",
            "scrap_pattern": re.compile("link-0-"),
        }
    }
    URL_HREF_PATTERN = re.compile("href=(?P<url>)")
    LIST_PATTERN = re.compile("List .* (?P<symbol>\((\w+\)))")
    PAIR_PATTERN = re.compile("(?P<pair>\w+/\w+)")


class ScrapBinance(BaseScrap):
    def __init__(self, scrap_option: str):
        self.base_url = self.SCRAP_URLS.get(scrap_option)["base_url"]
        self.url = (
            f'{self.base_url}{self.SCRAP_URLS.get(scrap_option)["announcement_path"]}'
        )
        self.url_pattern = self.SCRAP_URLS.get(scrap_option)["scrap_pattern"]
        if not self.url:
            raise ValueError(f"{scrap_option} not a valid option")
        self.link_content = {}

    @property
    def _raw_content(self):
        page = requests.get(self.url)
        if not page:
            raise ValueError(f"There was a problem with the connection to {self.url}")
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    @property
    def text_content(self):
        content = self._raw_content.findAll("a", id=self.url_pattern)
        return [item.text for item in content]

    @property
    def url_content(self):
        content = self._raw_content.find_all("a", id=self.url_pattern)
        dict_urls = {item.text: f"{self.base_url}{item['href']}" for item in content}
        temp_dict = dict_urls.copy()
        for text, url in temp_dict.items():
            match_list = self.LIST_PATTERN.search(text)
            match_pair = self.PAIR_PATTERN.findall(text)
            if not match_list and not match_pair:
                dict_urls.pop(text)
        return dict_urls

    @property
    def direct_list_tokens(self):
        """
        Scrapes new listings page for and returns new Symbol when appropriate
        """
        direct_list_tokens = []
        for line in self.text_content:
            match_pattern = self.LIST_PATTERN.search(line)
            if match_pattern:
                try:
                    direct_list_tokens.append(match_pattern.group("symbol")[1:-1])
                except AttributeError:
                    pass
        return direct_list_tokens

    @property
    def new_pair_tokens(self):
        """
        Scrapes new pairs and returns new pairs when appropriate
        """
        new_pair_tokens = []
        for line in self.text_content:
            match_pattern = self.PAIR_PATTERN.findall(line)
            if match_pattern:
                for pair in match_pattern:
                    symbol1 = pair.split("/")[0]
                    symbol2 = pair.split("/")[1]
                    new_pair_tokens.append(symbol1)
                    new_pair_tokens.append(symbol2)
        return new_pair_tokens

    def get_last_coins(self):
        return self.direct_list_tokens + self.new_pair_tokens
