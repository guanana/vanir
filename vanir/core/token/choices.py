from django.db import models


class TokenTypes(models.TextChoices):
    BEP_20 = "BEP-20"
    ETH_ERC_20 = "ERC-20"
    ETH_ERC_223 = "ERC-223"
    ETH_ERC_721 = "ERC-721"
    ETH_ERC_777 = "ERC-777"
    ETH_ERC_820 = "ERC-820"
    ETH_ERC_1155 = "ERC-1155"
    SOL_SPL = "SPL"
    EOS_EOSIO = "EOSIO"
    TEZOS_TZIP = "TZIP"
    NEO_NEP = "NEP"
    OTHER = "OTHER"
