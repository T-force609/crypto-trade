from django.urls import re_path
from market import consumers

websocket_urlpatterns = [
    re_path(r"ws/prices/$", consumers.PriceConsumer.as_asgi()),
]
