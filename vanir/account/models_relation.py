from datetime import datetime

from django.db import models


class AccountTokens(models.Model):
    """
    Relation between account and tokens
    """

    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    token = models.ForeignKey("token.Token", on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    update_time = models.TimeField(blank=True, null=True)
    # TODO: Last value needs to be in the relationship to be able
    #  to support different prices for different accounts!

    class Meta:
        unique_together = ("account", "token")

    def save(self, *args, **kwargs):
        token = AccountTokens.objects.filter(token=self.token)
        if token:
            self.update_time = datetime.now()
            super(AccountTokens, self).save(*args, **kwargs)
        else:
            super(AccountTokens, self).save(*args, **kwargs)
