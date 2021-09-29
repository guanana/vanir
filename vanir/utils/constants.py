from collections import OrderedDict

from vanir.core.account.filtersets import AccountFilterSet
from vanir.core.account.models import Account
from vanir.core.account.tables import AccountTable
from vanir.core.blockchain.filtersets import BlockchainFilterSet
from vanir.core.blockchain.models import Blockchain
from vanir.core.blockchain.tables import BlockchainTable
from vanir.core.exchange.filtersets import ExchangeFilterSet
from vanir.core.exchange.models import Exchange
from vanir.core.exchange.tables import ExchangeTable
from vanir.core.token.models import Token
from vanir.core.token.tables import TokenTable

SEARCH_MAX_RESULTS = 15
SEARCH_TYPES = OrderedDict(
    (
        (
            "account",
            {
                "queryset": Account.objects.prefetch_related("token"),
                "filterset": AccountFilterSet,
                "table": AccountTable,
                "url": "account:account_list",
            },
        ),
        (
            "blockchain",
            {
                "queryset": Blockchain.objects.all(),
                "filterset": BlockchainFilterSet,
                "table": BlockchainTable,
                "url": "blockchain:blockchain_list",
            },
        ),
        (
            "exchange",
            {
                "queryset": Exchange.objects.prefetch_related("provider"),
                "filterset": ExchangeFilterSet,
                "table": ExchangeTable,
                "url": "exchange:exchange_list",
            },
        ),
        (
            "token",
            {
                "queryset": Token.objects.prefetch_related("accounttokens_set"),
                "filterset": "TokenFilterSet",
                "table": TokenTable,
                "url": "token:token_list",
            },
        ),
    )
)
