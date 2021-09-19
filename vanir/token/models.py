from django.db import models

from vanir.blockchain.models import Blockchain
from vanir.token.choices import TokenTypes
from vanir.utils.models import BaseObject


class Coin(BaseObject):
    name = models.CharField(max_length=40)
    symbol = models.CharField(max_length=6)
    blockchain = models.ForeignKey(Blockchain, on_delete=models.CASCADE)
    decimals = models.IntegerField(default=10)

    def __str__(self):
        return self.symbol

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('token:coin_detail', kwargs={'pk': self.pk})


class Token(Coin):
    token_type = models.CharField(max_length=9, choices=TokenTypes.choices)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('token:token_detail', kwargs={'pk': self.pk})
