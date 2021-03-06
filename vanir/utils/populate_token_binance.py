import logging

from django.core.exceptions import ValidationError

from vanir.core.account.models import Account
from vanir.core.blockchain.models import Blockchain
from vanir.core.exchange.libs.exchanges import VanirBinance
from vanir.core.token.helpers.import_utils import bulk_update, token_import

logger = logging.getLogger(__name__)


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
        for symbol in self.con.get_asset_details().keys():
            token = token_import(
                account=self.account, token_symbol=symbol, token_fullname=symbol
            )
            self.tokens.append(token)
        bulk_update(self.account)
