from django import forms

from vanir.account.models import Account
from vanir.utils.populate_token_binance import PopulateDBBinance


def validate_account(account):
    """
    Trying to instantiate the class to raise errors if any
    """
    PopulateDBBinance(account)


class PopulateDBBinanceForm(forms.Form):
    account = forms.ModelChoiceField(
        queryset=Account.objects.filter(exchange__name__contains="Binance"),
        validators=[validate_account],
    )

    def populate_db(self):
        PopulateDBBinance(self.cleaned_data["account"]).create_all_tokens()
