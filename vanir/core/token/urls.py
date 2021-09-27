from django.urls import path

from .views import (
    TokenBulkUpdateValueView,
    TokenCreateView,
    TokenDeleteView,
    TokenDetailUpdateValueView,
    TokenDetailView,
    TokenListView,
    TokenUpdateView,
)

app_name = "token"
urlpatterns = [
    path("", TokenListView.as_view(), name="token_list"),
    path("add/", TokenCreateView.as_view(), name="token_add"),
    path(
        "bulk_update_price/",
        TokenBulkUpdateValueView.as_view(),
        name="token_bulk_update_price",
    ),
    path("<int:pk>/", TokenDetailView.as_view(), name="token_detail"),
    path("<int:pk>/edit/", TokenUpdateView.as_view(), name="token_update"),
    path("<int:pk>/delete/", TokenDeleteView.as_view(), name="token_delete"),
    path(
        "<int:pk>/update_price/",
        TokenDetailUpdateValueView.as_view(),
        name="token_update_price",
    ),
]
