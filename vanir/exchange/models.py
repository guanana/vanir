from decimal import Decimal
from django.db import models
from vanir.token.models import Token


class Exchange(models.Model):
    name = models.CharField(max_length=250)
    default_fee = models.DecimalField(
        max_digits=30, decimal_places=4, default=Decimal(0.1)
    )
    native_token = models.ForeignKey(Token, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

