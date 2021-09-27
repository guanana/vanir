from django.urls import path
from django.views.generic import TemplateView

from .views import (
    AccountCreateView,
    AccountDeleteView,
    AccountDetailView,
    AccountListView,
    AccountTokenBulkUpdateValueView,
    AccountUpdateView,
    delete_tokens_account,
    exchange_balanceview,
    exchange_importtokens,
    exchange_testview,
)

app_name = "account"
urlpatterns = [
    path("", AccountListView.as_view(), name="account_list"),
    path("add/", AccountCreateView.as_view(), name="account_add"),
    path("<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    path("<int:pk>/edit/", AccountUpdateView.as_view(), name="account_update"),
    path("<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"),
    path(
        "<int:pk>/refresh/",
        AccountTokenBulkUpdateValueView.as_view(),
        name="account_refresh",
    ),
    path("<int:pk>/test/", exchange_testview, name="account_test"),
    path(
        "<int:pk>/delete_tokens/", delete_tokens_account, name="account_delete_tokens"
    ),
    path("<int:pk>/balance/", exchange_balanceview, name="account_balance"),
    path(
        "<int:pk>/balance/import/", exchange_importtokens, name="account_balance_import"
    ),
    path(
        "<int:pk>/more/",
        TemplateView.as_view(template_name="account/account_more.html"),
        name="account_more",
    ),
]
