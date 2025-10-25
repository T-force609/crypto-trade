from django.urls import path
from .views import TradeView
from . import views

urlpatterns = [
    path('', TradeView.as_view(), name='trade'),
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'), # implement to return WalletSerializer
    path('transactions/', views.TransactionListView.as_view(), name='transactions'),
]
