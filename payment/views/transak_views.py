from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from payment.views.base_views import create_transaction, success_response

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_transak_payment(request):
    amount = request.data.get("amount")
    currency = request.data.get("currency", "USD")

    tx = create_transaction(request.user, "transak", amount, currency)

    widget_url = f"https://global.transak.com?apiKey=YOUR_TRANSAK_API_KEY&fiatAmount={amount}&fiatCurrency={currency}&partnerOrderId={tx.id}"
    return success_response({"widget_url": widget_url})
