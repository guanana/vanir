from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db import models

from vanir.core.blockchain.models import Blockchain
from vanir.core.token.models import Token
from vanir.utils.models import BaseObject


class Exchange(BaseObject):
    default_fee = models.DecimalField(max_digits=30, decimal_places=4, default=0.1)
    native_token = models.ForeignKey(
        Token, on_delete=models.deletion.SET_NULL, null=True, blank=True
    )
    default_blockchain = models.ForeignKey(
        Blockchain, on_delete=models.CASCADE, null=True
    )


class AllowedPairs(models.Model):
    """
    TODO: Check how if this is possible in future
    Pretend to use it for get a general table with history of price but
    multiple challenges to overcome, like speed (BulkUpdateOrCreateQuerySet) helped
    there and history (HistoricalRecords) not being updated because BulkUpdateOrCreateQuerySet not
    sending signal. Not used for now, left here for ref
    """

    source = models.CharField(max_length=40, default="Binance")
    pair = models.CharField(max_length=15, unique=True)
    price = models.DecimalField(max_digits=30, decimal_places=8, null=True)
    # history = HistoricalRecords()
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    # Make it abstract for now to now have the tables created
    class Meta:
        abstract = True

    def __str__(self):
        return self.pair

    def natural_key(self):
        return (self.pair,)
