from django.contrib import admin

from vanir.core.token.models import Coin, Token

admin.site.register(Token)
admin.site.register(Coin)
