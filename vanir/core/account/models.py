from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import SET_NULL
from django.utils.functional import cached_property

from vanir.core.exchange.libs.exchanges import ExtendedExchangeRegistry
from vanir.core.exchange.models import Exchange
from vanir.core.token.models import Token
from vanir.users.admin import User
from vanir.utils.helpers import value_pair
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
    default_fee_rate = models.FloatField(default=0.1)
    token = models.ManyToManyField(
        "token.Token", through="AccountTokens", related_name="accounts"
    )
    token_pair = models.ForeignKey(
        Token, on_delete=SET_NULL, null=True, related_name="token_pair"
    )
    default = models.BooleanField(
        default=False,
        help_text="Default account to run fetch methods like token price update",
    )
    testnet = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.check_default()
        super().save(*args, **kwargs)

    def check_default(self):
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

    def clear_tokens(self):
        self.accounttokens_set.all().delete()

    @cached_property
    def exchange_obj(self):
        try:
            class_obj = ExtendedExchangeRegistry.get_class_by_name(
                self.exchange.name.split(" ")[0]
            )
        except KeyError:
            raise ValidationError(
                f"Please create an account with a supported Exchange to get extra functionalities"
                f"{[item for item in ExtendedExchangeRegistry.registered.keys()]}"
            )
        return class_obj(self)

    @property
    def total_value_account(self):
        total_value = 0
        tokens_not_found = []
        price_dict = self.exchange_obj.all_assets_prices
        for token_account in self.accounttokens_set.all():
            token_obj = token_account.token
            pair = value_pair(token_obj, self.token_pair)
            try:
                total_value += price_dict[pair] * token_account.quantity
            except KeyError:
                tokens_not_found.append(token_obj.name)
        return round(total_value, 2)

    @property
    def total_value_account_table(self):
        return f"{self.total_value_account} {self.token_pair}"
