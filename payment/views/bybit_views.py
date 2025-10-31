from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .base_views import success_response, create_transaction


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_bybit_payment(request):
    amount = request.data.get("amount")
    currency = request.data.get("currency", "USD")
    tx = create_transaction(request.user, "bybit", amount, currency)
    # Initiate Bybit fiat deposit using their API (if available) or redirect user to Bybit on-ramp link
    deposit_link = generate_bybit_deposit_link(user=request.user, amount=amount, currency=currency, partnerId=tx.id)
    return success_response({"deposit_link": deposit_link})
