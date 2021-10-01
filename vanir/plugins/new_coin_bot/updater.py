from apscheduler.schedulers.background import BackgroundScheduler

from .scrappers import ScrapBinance


def start():
    scrap_obj = ScrapBinance()
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrap_obj.import_token_announcements(), "interval", minutes=5)
    scheduler.start()
