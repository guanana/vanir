from django.urls import path

from .views import TokenListView, TokenUpdateView, TokenDetailView, TokenDeleteView, TokenCreateView

app_name = "token"
urlpatterns = [
        path('', TokenListView.as_view(), name="token_list"),
        path('add/', TokenCreateView.as_view(), name="token_add"),
        path('<int:pk>/', TokenDetailView.as_view(), name='token_detail'),
        path('<int:pk>/edit/', TokenUpdateView.as_view(), name='token_update'),
        path('<int:pk>/delete/', TokenDeleteView.as_view(), name='token_delete'),
]
