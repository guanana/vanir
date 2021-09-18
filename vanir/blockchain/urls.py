from django.urls import path

from .views import BlockchainListView, BlockchainCreateView, BlockchainUpdateView, BlockchainDetailView, BlockchainDeleteView

app_name = "blockchain"
urlpatterns = [
        path('', BlockchainListView.as_view(), name="blockchain_list"),
        path('add/', BlockchainCreateView.as_view(), name="blockchain_add"),
        path('edit/<int:pk>/', BlockchainUpdateView.as_view(), name='blockchain_update'),
        path('<int:pk>/', BlockchainDetailView.as_view(), name='blockchain_detail'),
        path('delete/<int:pk>/', BlockchainDeleteView.as_view(), name='blockchain_delete'),

]
