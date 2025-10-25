from django.urls import path
from .views import MarketPricesView

urlpatterns = [
    path('', MarketPricesView.as_view(), name='market-prices'),
]
