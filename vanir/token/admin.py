from django.contrib import admin

from vanir.token.models import Token, Coin

admin.site.register(Token)
admin.site.register(Coin)

