from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import SET_NULL
from django.utils.functional import cached_property
from simple_history.models import HistoricalRecords

from vanir.core.token.models import Token
from vanir.utils.datasource.coingecko import CoinGeckoVanir
from vanir.utils.datasource.fiat_convertor import FiatConvertorVanir
from vanir.utils.exceptions import ExchangeExtendedFunctionalityError
from vanir.utils.helpers import fetch_exchange_obj
from vanir.utils.models import BaseObject, TimeStampedMixin


class Account(BaseObject):
    """Exchange Account"""

    exchange = models.ForeignKey(
        "exchange.Exchange", on_delete=models.CASCADE, null=False
    )
    extended_exchange = models.BooleanField(editable=False, default=False)
    api_key = models.CharField(
        max_length=250,
        help_text="API key for the exchange, do not touch if you're adding a manual exchange",
        default="None",
    )
    secret = models.CharField(
        max_length=250,
        help_text="API secret for the exchange, do not touch if you're adding a manual exchange",
        default="None",
    )
    tld = models.CharField(max_length=10, default="com")
    default_fee_rate = models.FloatField(default=0.1)
    token = models.ManyToManyField(
        "token.Token", through="AccountTokens", related_name="accounts"
    )
    token_pair = models.ForeignKey(
        Token,
        on_delete=SET_NULL,
        null=True,
        related_name="token_pair",
        help_text="Choose a token to be your pair value",
    )
    default = models.BooleanField(
        default=False,
        help_text="Default account to run fetch methods like token price update",
    )
    testnet = models.BooleanField(
        default=False, help_text="Only for test accounts with DEV accounts"
    )

    class Meta:
        ordering = ["name"]

    def clean(self):
        """Clean the object before saving"""
        if self.exchange_obj:
            if not self.exchange_obj.test():
                raise ValidationError(
                    "Api key and Secret are not correct, unable to connect"
                )

    def save(self, *args, **kwargs):
        """
        Saves account but first checks if it's extended exchange
        and if there's another account with default=True and corrects
        problem of 2 accounts being default.
        """
        from vanir.core.account.helpers.balance import update_balance

        if self._state.adding:
            self.is_extended_exchange()
            self.check_default()
            update_balance(self)
        elif self.pk is not None:
            orig = Account.objects.get(pk=self.pk)
            if orig.token_pair != self.token_pair:
                update_balance(self)
        super().save(*args, **kwargs)

    def check_default(self):
        """
        Check if there are more accounts with default setting
        if there is another (can only be one). Remove the default
        flag and add it to the new one
        """
        if self.default:
            for account in Account.objects.all():
                if account.default and account != self:
                    account.default = False
                    account.save()
        # In case is the first account always set up as default
        if Account.objects.count() == 0:
            self.default = True

    def clear_tokens(self):
        """
        Remove all the tokens assigned to an account
        """
        self.accounttokens_set.all().delete()

    def is_extended_exchange(self):
        """
        Checks if the exchange is "supported" or not
        :return: If it's or not an extended/supported exchange
        :rtype: bool
        """
        if isinstance(self.exchange_obj, CoinGeckoVanir):
            return False
        else:
            return True

    @cached_property
    def exchange_obj(self):
        """
        Checks and returns the appropriate object, for now either
        VanirBinance or CongeckoVanir
        :return: Appropriate object base on exchange
        :rtype: CoinGeckoVanir or VanirBinance
        """
        try:
            class_obj = fetch_exchange_obj(self.exchange.name)
            self.extended_exchange = True
        except ExchangeExtendedFunctionalityError:
            self.extended_exchange = False
            return CoinGeckoVanir()
        return class_obj(self)

    @property
    def total_value_account(self):
        """
        Calculates value of the account base on the tokens
        attach to it.
        :return: total value
        :rtype: float
        """
        total_value = 0
        for token_account in self.accounttokens_set.all():
            try:
                total_value += token_account.token.last_value * token_account.quantity
            except KeyError:
                pass
        return round(total_value, 4)

    @property
    def total_value_account_table(self):
        """
        Property used by the table to display the value
        with the appropriate token pair
        :return: Value + Token
        :rtype: str
        """
        return f"{round(self.total_value_account * self.get_value_factor, ndigits=2) } {self.token_pair}"

    @cached_property
    def get_value_factor(self):
        """
        Get the factor to multiply by base on the pair token
        :return: factor
        :rtype: float
        """
        fc = FiatConvertorVanir()
        return fc.convert_from(self.token_pair.symbol)


class AccountTokens(TimeStampedMixin):
    """Relation between account and tokens"""

    id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    token = models.ForeignKey("token.Token", on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    history = HistoricalRecords()

    class Meta:
        unique_together = ("account", "token")

    def get_absolute_url(self):
        return self.account.get_absolute_url()

    @staticmethod
    def get_title():
        """
        Use by templates to get title instead of class name
        :rtype: str
        """
        return "tokens to the account"
