from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework.permissions import AllowAny

class MarketPricesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        # Example: request top N coins from CoinGecko
        vs_currency = request.query_params.get("vs", "usd")
        ids = request.query_params.get("ids", None)
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency": vs_currency, "order": "market_cap_desc", "per_page": 50, "page": 1}
        if ids: params["ids"] = ids
        r = requests.get(url, params=params, timeout=10)
        return Response(r.json())
