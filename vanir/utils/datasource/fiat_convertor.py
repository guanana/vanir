import json

import requests


class FiatConvertorVanir():
    def __init__(self, base_fiat: str = "USD"):
        self.base_url = "https://open.er-api.com/v6/latest/"
        self.base_fiat = base_fiat

    def rates(self):
        """
        Get api content, defaults to USD
        :return: dictionary object with api data
        :rtype: dict
        """
        url = f"{self.base_url}{self.base_fiat}"
        page = requests.get(url, headers={"User-Agent": ""})
        if not page:
            raise ValueError(f"There was a problem with the connection to {url}")
        data = json.loads(page.content)
        try:
            rate = data["rates"]
        except KeyError:
            return
        return rate

    def convert_from(self, fiat_into: str, quantity: float = 1):
        """
        Get the price for the specified fiat
        :param quantity: Quantity to convert
        :param fiat_into: Fiat to convert
        :return: price
        :rtype: float
        """
        fiat_into = fiat_into.upper()
        try:
            usd_to_fiat = self.rates()[fiat_into]
            return usd_to_fiat * quantity
        except KeyError:
            return 0
