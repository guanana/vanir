from django.contrib import admin

from .models import LimitOrder, MarketOrder, StopLossOrTakeProfitLimitOrder, StopPriceOrder

admin.site.register(LimitOrder)
admin.site.register(MarketOrder)
admin.site.register(StopPriceOrder)
admin.site.register(StopLossOrTakeProfitLimitOrder)
