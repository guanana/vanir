from django.contrib import admin

# Register your models here.
from vanir.plugins.new_coin_bot.models import BinanceNewToken, NewCoinConfig

admin.site.register(NewCoinConfig)
admin.site.register(BinanceNewToken)
