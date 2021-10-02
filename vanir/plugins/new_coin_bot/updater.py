from apscheduler.schedulers.background import BackgroundScheduler

from vanir.plugins.new_coin_bot.scrappers_model import ScrapBinanceModel


def start():
    scrap_obj = ScrapBinanceModel()
    scheduler = BackgroundScheduler()
    scrapbinancemodel_job = scheduler.add_job(  # noqa F841
        scrap_obj.import_token_announcements(), "interval", minutes=10
    )
    scheduler.start()
