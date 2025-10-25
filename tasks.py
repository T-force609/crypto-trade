from celery import shared_task
import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@shared_task
def fetch_and_broadcast_prices():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency":"usd","order":"market_cap_desc","per_page":50,"page":1}
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "prices",
        {"type":"price.update", "data": data}
    )
