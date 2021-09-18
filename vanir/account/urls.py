from django.urls import path

from .views import AccountListView, AccountCreateView, AccountUpdateView, AccountDetailView, AccountDeleteView

app_name = "account"
urlpatterns = [
        path('', AccountListView.as_view(), name="account_list"),
        path('add/', AccountCreateView.as_view(), name="account_add"),
        path('<int:pk>/', AccountDetailView.as_view(), name='account_detail'),
        path('<int:pk>/edit/', AccountUpdateView.as_view(), name='account_update'),
        path('<int:pk>/delete/', AccountDeleteView.as_view(), name='account_delete'),

]
