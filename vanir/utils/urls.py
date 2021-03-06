from django.urls import path

from vanir.utils.views import PopulateDBBinanceView

app_name = "utils"
urlpatterns = [
    path(
        "populate_db_binance/",
        PopulateDBBinanceView.as_view(),
        name="utils_populate_db_binance",
    ),
]
