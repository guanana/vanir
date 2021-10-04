from django.db import models


class DiscoverMethod(models.TextChoices):
    BINANCE_SCRAPPER = "Binance Scrapper"
    MANUAL = "Manual"
    OTHER = "Other"


class ScrapperOptions(models.TextChoices):
    BINANCE_SCRAPPER = "ScrapBinanceModelWithDate"


class ScheduleScrap(models.IntegerChoices):
    EVERY_2_MINS = 2
    EVERY_5_MINS = 5
    EVERY_10_MINS = 10
    EVERY_15_MINS = 15
    EVERY_20_MINS = 20
    EVERY_30_MINS = 30
    EVERY_50_MINS = 50
    EVERY_1_HOUR = 60
    EVERY_1_AND_HALF_HOURS = 90
    EVERY_2_HOURS = 120
