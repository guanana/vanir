from django import forms
from django.core.exceptions import ValidationError
from django.views.generic import FormView

from vanir.account.models import Account
from vanir.blockchain.models import Blockchain
from vanir.exchange.libs.exchanges import VanirBinance
from vanir.token.helpers.import_utils import bulk_update
from vanir.token.models import Token


class PopulateDBBinance:
    def __init__(self, account: Account):
        self.account = account
        if self.account.testnet:
            raise ValidationError("You cannot populate DB with test account")
        self.con = VanirBinance(self.account)
        self.tokens = []

    @property
    def blockchain(self):
        blockchain, created = Blockchain.objects.get_or_create(
            name="Binance",
            project_url="https://www.binance.org/en/smartChain",
            explorer_url="https://bscscan.com/",
        )
        blockchain.save()
        return blockchain

    def create_all_tokens(self):
        for symbol, fullname in self.con.all_margin_assets.items():
            token, created = Token.objects.get_or_create(
                name=fullname, symbol=symbol, blockchain=self.blockchain
            )
            self.tokens.append(token)
        bulk_update(self.account)


def validate_account(account):
    PopulateDBBinance(account)


class PopulateDBBinanceForm(forms.Form):
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(), validators=[validate_account]
    )

    def populate_db(self):
        PopulateDBBinance(self.cleaned_data["account"]).create_all_tokens()


class PopulateDBBinanceView(FormView):
    form_class = PopulateDBBinanceForm
    template_name = "basic_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Populate DB with Binance"
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.populate_db()
        return super().form_valid(form)
