from django.urls import path

from .views import (
    AccountCreateView,
    AccountDeleteView,
    AccountDetailView,
    AccountListView,
    AccountUpdateView,
    exchangebalanceview,
    exchangetestview,
)

app_name = "account"
urlpatterns = [
    path("", AccountListView.as_view(), name="account_list"),
    path("add/", AccountCreateView.as_view(), name="account_add"),
    path("<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
    path("<int:pk>/edit/", AccountUpdateView.as_view(), name="account_update"),
    path("<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"),
    path("<int:pk>/test/", exchangetestview, name="account_test"),
    path("<int:pk>/balance/", exchangebalanceview, name="account_balance"),
]
