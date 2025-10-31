import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from payment.views.base_views import create_transaction, success_response, error_response

COINBASE_API_URL = "https://api.commerce.coinbase.com/charges"
COINBASE_API_KEY = "organizations/b76d0552-f615-4792-bbc6-fe015ffc0337/apiKeys/b95d049e-dea7-4385-99f6-a67a96e7b717"

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_coinbase_payment(request):
    amount = request.data.get("amount")
    currency = request.data.get("currency", "USD")

    tx = create_transaction(request.user, "coinbase", amount, currency)

    payload = {
        "name": "Crypto Deposit",
        "description": "Deposit funds to your trading account",
        "pricing_type": "fixed_price",
        "local_price": {"amount": str(amount), "currency": currency},
        "metadata": {"transaction_id": tx.id},
    }

    headers = {"X-CC-Api-Key": COINBASE_API_KEY, "Content-Type": "application/json"}

    r = requests.post(COINBASE_API_URL, json=payload, headers=headers)
    if r.status_code == 201:
        response_data = r.json()
        checkout_url = response_data["data"]["hosted_url"]
        return success_response({"checkout_url": checkout_url})
    else:
        return error_response("Failed to initiate Coinbase payment.")
