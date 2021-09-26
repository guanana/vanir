import logging

from django.core.exceptions import ValidationError

from vanir.account.models import Account
from vanir.blockchain.models import Blockchain
from vanir.exchange.libs.exchanges import VanirBinance
from vanir.token.helpers.import_utils import bulk_update
from vanir.token.models import Token

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
        for symbol, fullname in self.con.all_margin_assets.items():
            try:
                token = Token.objects.get(symbol=symbol)
                if token.name != fullname:
                    logger.info("Updating token name")
                    token.name = fullname
                    token.save()
            except Token.DoesNotExist:
                token = Token.objects.create(
                    name=fullname, symbol=symbol, blockchain=self.blockchain
                )
            self.tokens.append(token)
        bulk_update(self.account)
