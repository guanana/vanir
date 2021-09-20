from django.db import models

from vanir.token.models import Token


class AccountTokens(models.Model):
    """
    Relation between account and tokens
    """

    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=30, decimal_places=4, default=0.01)
    update_time = models.TimeField(auto_now=True)
