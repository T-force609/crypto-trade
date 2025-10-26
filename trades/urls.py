from django.urls import path
from .views import TradeView
from . import views
from .views import DepositCreateAPIView

urlpatterns = [
    path('', TradeView.as_view(), name='trade'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'), # implement to return WalletSerializer
    path('transactions/', views.TransactionListCreateAPIView.as_view(), name='transactions'), # implement to return list of transactions
    path('deposits/', DepositCreateAPIView.as_view(), name='deposit-create')
]
