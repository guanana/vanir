from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "account"
urlpatterns = [
    path("", views.AccountListView.as_view(), name="account_list"),
    path("add/", views.AccountCreateView.as_view(), name="account_add"),
    path("<int:pk>/", views.AccountDetailView.as_view(), name="account_detail"),
    path("<int:pk>/edit/", views.AccountUpdateView.as_view(), name="account_edit"),
    path(
        "<int:pk>/tokens/add/",
        views.AccountTokensCreateView.as_view(),
        name="account_tokens_add",
    ),
    path("<int:pk>/delete/", views.AccountDeleteView.as_view(), name="account_delete"),
    path(
        "<int:pk>/refresh/",
        views.AccountTokenBulkUpdateValueView.as_view(),
        name="account_refresh",
    ),
    path("<int:pk>/test/", views.exchange_testview, name="account_test"),
    path(
        "<int:pk>/delete_tokens/",
        views.delete_tokens_account,
        name="account_delete_tokens",
    ),
    path("<int:pk>/balance/", views.exchange_balanceview, name="account_balance"),
    path(
        "<int:pk>/balance/import/",
        views.exchange_importtokens,
        name="account_balance_import",
    ),
    path(
        "<int:pk>/more/",
        TemplateView.as_view(template_name="account/account_more.html"),
        name="account_more",
    ),
]
