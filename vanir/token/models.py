from django.db import models

from vanir.blockchain.models import Blockchain
from vanir.token.choices import TokenTypes


class Coin(models.Model):
    name = models.CharField(max_length=40)
    symbol = models.CharField(max_length=6)
    blockchain = models.ForeignKey(Blockchain, on_delete=models.CASCADE)
    decimals = models.IntegerField(default=10)

    def __str__(self):
        return self.symbol


class Token(Coin):
    token_type = models.CharField(max_length=9, choices=TokenTypes.choices)
