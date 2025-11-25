from django.urls import path
from . import views

urlpatterns = [
    path('coinbase/start/', views.coinbase_start, name='coinbase_start'),
    path('kraken/start/', views.kraken_start, name='kraken_start'),
    path('binance/start/', views.binance_start, name='binance_start'),
    path('gemini/start/', views.gemini_start, name='gemini_start'),
    path('ramp/start/', views.ramp_start, name='ramp_start'),
    path('crypto_com/start/', views.crypto_com_start, name='crypto_com_start'),
]
