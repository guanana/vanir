import json
import logging

from celery import shared_task
from django.db import models
from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from vanir.core.token.models import Coin, Token
from vanir.plugins.models import PluginBase
from vanir.plugins.new_coin_bot.choices import (
    DiscoverMethod,
    ScheduleScrap,
    ScrapperOptions,
)
from vanir.plugins.new_coin_bot.helpers import token_already_exists
from vanir.plugins.new_coin_bot.scrappers import ScrapBinance
from vanir.utils.models import TimeStampedMixin

logger = logging.getLogger(__name__)


class ScrapBinanceModel(ScrapBinance):
    DISCOVER_METHOD = "Binance Scrapper"

    def _clean(self):
        return self._remove_existing_tokens()

    def _remove_existing_tokens(self):
        final_list = list()
        for token_symbol in self._last_token_announcements:
            if not token_already_exists(token_symbol):
                final_list.append(token_symbol)
        return final_list

    def import_token_announcements(self):
        import_list = self._clean()
        for token_symbol in import_list:
            new_coin, created = BinanceNewToken.objects.get_or_create(
                name=token_symbol, symbol=token_symbol
            )
            new_coin.discovered_method = self.DISCOVER_METHOD
            new_coin.listing_day = self.release_date(self.match_lines[token_symbol])

            new_coin.increase_announcement_seen()
            new_coin.save()
            if created:
                logger.info(f"Token {token_symbol} added")
            else:
                logger.info(f"Token {token_symbol} updated")

    @shared_task(name="ScrapBinanceModelWithDate")
    def run(self):
        logger.info(f"Running {self.__class__.__name__}")
        self.import_token_announcements()
        logger.info("Run finished")


class NewCoinConfig(PluginBase, TimeStampedMixin):
    scrapper_class_name = models.CharField(
        unique=True,
        choices=ScrapperOptions.choices,
        max_length=100,
        verbose_name="Scrapper",
    )
    scrapping_interval = models.IntegerField(choices=ScheduleScrap.choices, default=10)
    auto_clean = models.BooleanField(
        default=True,
        help_text="The tokens that are more than 2 days old will "
        "be promoted to regular tokens automatically",
    )
    activate_scheduler = models.BooleanField(default=False)
    task = models.OneToOneField(
        PeriodicTask, on_delete=models.CASCADE, null=True, blank=True
    )
    task_auto_clean = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="task_auto_clean",
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.name = self.scrapper_class_name
            IntervalSchedule.objects.create(
                every=self.scrapping_interval, period="minutes"
            )
        self.task, created = PeriodicTask.objects.get_or_create(
            name=self.scrapper_class_name,
            task=self.scrapper_class_name,
            interval=IntervalSchedule.objects.get(
                every=self.scrapping_interval, period="minutes"
            ),
            args=json.dumps([self.scrapper_class_name]),
            start_time=timezone.now(),
        )
        self.task.enabled = self.activate_scheduler
        self.task.save()

        self.task_auto_clean, created_auto_clean = PeriodicTask.objects.get_or_create(
            name=f"{self.scrapper_class_name}_auto_clean",
            task=f"{self.scrapper_class_name}_auto_clean",
            interval=IntervalSchedule.objects.get(
                every=self.scrapping_interval, period="minutes"
            ),
            args=json.dumps([f"{self.scrapper_class_name}_auto_clean"]),
            start_time=timezone.now(),
        )
        self.task_auto_clean = self.auto_clean
        super().save(*args, **kwargs)


class NewCoin(PluginBase, Coin, TimeStampedMixin):
    discovered_method = models.CharField(max_length=25, choices=DiscoverMethod.choices)
    listing_day = models.DateTimeField(null=True)
    announcement_seen = models.IntegerField(null=True, default=0)

    class Meta:
        abstract = True
        unique_together = ("name", "symbol")

    def increase_announcement_seen(self):
        self.announcement_seen += 1
        self.save()

    @property
    def is_new(self):
        if self.announcement_seen <= 1:
            return True
        return False

    def promote_to_standard_token(self):
        """
        Creates a token in the core DB and removes itself from the NewCoinModel
        """
        token_obj = Token.objects.create(name=self.name, symbol=self.symbol)
        token_obj.set_value()
        self.delete()
        return token_obj


class BinanceNewToken(NewCoin):
    discovered_method = models.CharField(
        max_length=25, choices=DiscoverMethod.choices, default="Binance Scrapper"
    )
