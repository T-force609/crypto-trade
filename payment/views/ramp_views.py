from rest_framework.permissions import IsAuthenticated
from payment.views.base_views import create_transaction, success_response
from rest_framework.decorators import api_view, permission_classes

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_ramp_payment(request):
    amount = request.data.get("amount")
    currency = request.data.get("currency", "USD")
    tx = create_transaction(request.user, "ramp", amount, currency)
    # Generate widget URL or API call to Ramp
    # (Using hostApiKey etc.)
    widget_url = f"https://ramp.network/?hostApiKey={YOUR_RAMP_API_KEY}&fiatAmount={amount}&fiatCurrency={currency}&partnerTransactionId={tx.id}"
    return success_response({"widget_url": widget_url})
