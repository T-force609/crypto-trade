from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .base_views import create_transaction, success_response

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_crypto_com_payment(request):
    amount = request.data.get("amount")
    currency = request.data.get("currency", "USD")
    tx = create_transaction(request.user, "crypto_com", amount, currency)
    # Call Crypto.com Pay API
    payload = {
        "amount": str(amount),
        "currency": currency,
        "description": "Deposit funds",
        "merchant_transaction_id": tx.id,
    }
    # Use secret key to call POST https://pay.crypto.com/api/payments
    # Parse response, get payment_id etc.
    return success_response({"payment_id": payment_id, "checkout_url": checkout_url})
