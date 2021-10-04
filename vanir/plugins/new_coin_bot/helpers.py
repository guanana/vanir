import datetime
import logging

from celery import shared_task

from vanir.core.token.models import Token

logger = logging.getLogger(__name__)


def token_already_exists(symbol):
    try:
        Token.objects.get(symbol=symbol)
        logger.info(f"Token {symbol} already in DB, skipping...")
        return True
    except Token.DoesNotExist:
        return False


@shared_task(name="ScrapBinanceModelWithDate_auto_clean")
def auto_promote():
    from .models import BinanceNewToken

    for new_token in BinanceNewToken.objects.filter(
        listing_day__gte=datetime.timedelta(days=2)
    ):
        new_token.promote_to_standard_token()
