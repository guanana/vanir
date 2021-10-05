import logging
from datetime import timedelta

from celery import shared_task

from vanir.core.token.models import Token

logger = logging.getLogger(__name__)


def token_already_exists(symbol):
    try:
        Token.objects.get(symbol=symbol)
        logger.debug(f"Token {symbol} already in DB, skipping...")
        return True
    except Token.DoesNotExist:
        return False


@shared_task(name="ScrapBinanceModel_auto_clean")
def auto_promote():
    from .models import BinanceNewToken

    for new_token in BinanceNewToken.objects.filter(listing_day__gte=timedelta(days=2)):
        new_token.promote_to_standard_token()


@shared_task(name="ScrapBinanceModel")
def run_scrap():
    from .models import ScrapBinanceModel

    obj = ScrapBinanceModel()
    logger.info(f"Running {obj.DISCOVER_METHOD}")
    obj.import_token_announcements()
    logger.info("Run finished")
