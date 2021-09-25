from datetime import datetime

from django.db import models

from vanir.token.models import Token


class AccountTokens(models.Model):
    """
    Relation between account and tokens
    """

    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    update_time = models.TimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        token = AccountTokens.objects.filter(token=self.token)
        if token:
            self.update_time = datetime.now()
        else:
            super().save(*args, **kwargs)
