from django.db import models


class DiscoverMethod(models.TextChoices):
    BINANCE_SCRAPPER = "Binance Scrapper"
    MANUAL = "Manual"
    OTHER = "Other"
