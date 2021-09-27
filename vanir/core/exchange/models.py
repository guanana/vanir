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
