# core/routing.py
from django.urls import path
from market.consumers import PriceConsumer

websocket_urlpatterns = [
    path("ws/prices/", PriceConsumer.as_asgi()),
]
