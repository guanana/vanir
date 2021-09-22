from django.db import models
from django.db.models import SET_NULL

from vanir.account.models_relation import AccountTokens
from vanir.exchange.models import Exchange
from vanir.token.models import Token
from vanir.users.admin import User
from vanir.utils.models import BaseObject


class Account(BaseObject):
    """
    Exchange Account
    """

    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=250)
    secret = models.CharField(max_length=250)
    tld = models.CharField(max_length=10, default="com")
    password = models.CharField(max_length=250, blank=True, null=True)
    default_fee_rate = models.DecimalField(
        max_digits=30, decimal_places=4, default=0.01
    )
    token = models.ManyToManyField(Token, through=AccountTokens)
    token_pair = models.ForeignKey(
        Token, on_delete=SET_NULL, null=True, related_name="token_pair"
    )
    default = models.BooleanField(
        default=False,
        help_text="Default account to run fetch methods like token price update",
    )
    testnet = models.BooleanField(default=False)

    @property
    def name(self):
        return f"{self.pk:02}-{self.exchange}-{self.user.get_username()}"

    def save(self, *args, **kwargs):
        # Check if there are more accounts with default setting
        # if there is another (can only be one). Remove the default
        # flag and add it to the new one
        if self.default:
            for account in Account.objects.all():
                if account.default and account != self:
                    account.default = False
                    account.save()
        # In case is the first account always set up as default
        if Account.objects.count() == 0:
            self.default = True
        super().save(*args, **kwargs)
