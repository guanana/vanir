from django.urls import include, path

app_name = "plugins"

urlpatterns = [
    path(
        "new_coin_bot/",
        include("vanir.plugins.new_coin_bot.urls", namespace="new_coin_bot"),
    ),
]
