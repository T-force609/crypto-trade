from django.urls import path
from .views import TradeView
from . import views
from .views import DepositCreateAPIView, DepositView, get_admin_wallet, create_deposit, get_wallets


urlpatterns = [
    path('', TradeView.as_view(), name='trade'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'), # implement to return WalletSerializer
    path('transactions/', views.TransactionListCreateAPIView.as_view(), name='transactions'), # implement to return list of transactions
    path('deposits/', DepositCreateAPIView.as_view(), name='deposit-create'),
    path("deposit/", create_deposit, name="create_deposit"),
    path("save_wallet_address/", views.save_wallet_address, name="save_wallet_address"),
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("admin-wallet/", get_admin_wallet, name="admin-wallet"),
    path("wallets/", get_wallets, name="list_wallets"),

]
