import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from payment.views.base_views import create_transaction, success_response, error_response

COINBASE_API_URL = "https://api.commerce.coinbase.com/charges"
COINBASE_API_KEY = "organizations/b76d0552-f615-4792-bbc6-fe015ffc0337/apiKeys/b95d049e-dea7-4385-99f6-a67a96e7b717"

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_coinbase_payment(request):
    try:
        amount = request.data.get("amount")
        currency = request.data.get("currency", "USD")
        crypto = request.data.get("crypto")  # BTC, ETH, etc.
        wallet_address = request.data.get("wallet_address")

        if not amount or not crypto or not wallet_address:
            return Response(
                {"error": "Missing required fields: amount, crypto, wallet_address"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create transaction record
        tx = create_transaction(request.user, "coinbase", amount, currency)

        payload = {
            "name": f"Buy {crypto}",
            "description": f"Purchase {crypto} and send to wallet {wallet_address}",
            "pricing_type": "fixed_price",
            "local_price": {"amount": str(amount), "currency": currency},
            "metadata": {
                "transaction_id": str(tx.id),
                "user_id": request.user.id,
                "crypto": crypto,
                "wallet_address": wallet_address,
            },
        }

        headers = {
            "X-CC-Api-Key": COINBASE_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(COINBASE_API_URL, json=payload, headers=headers)
        
        if response.status_code == 201:
            response_data = response.json()
            return success_response({
                "charge_id": response_data.get("id"),
                "hosted_url": response_data.get("hosted_url"),
                "transaction_id": tx.id,
            })
        else:
            return error_response(
                f"Coinbase error: {response.status_code}",
                status.HTTP_400_BAD_REQUEST
            )

    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def coinbase_webhook(request):
    """Handle Coinbase webhook for payment confirmation"""
    try:
        event = request.data
        
        if event.get("type") == "charge:confirmed":
            metadata = event.get("data", {}).get("metadata", {})
            transaction_id = metadata.get("transaction_id")
            
            # Update transaction status to completed
            # You'll need to implement this based on your Transaction model
            
            return Response({"status": "success"})
        
        return Response({"status": "received"})
    
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
