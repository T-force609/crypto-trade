import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
# Coinbase
OINBASE_API_URL = "https://api.commerce.coinbase.com/charges"



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def coinbase_start(request):
    try:
        amount = request.data.get("amount")
        currency = request.data.get("currency", "USD")
        crypto = request.data.get("crypto")
        wallet_address = request.data.get("wallet_address")

        if not all([amount, crypto, wallet_address]):
            return Response(
                {"error": "Missing required fields: amount, crypto, wallet_address"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use settings if you have set COINBASE_API_KEY in settings.py
        COINBASE_API_KEY = "organizations/b76d0552-f615-4792-bbc6-fe015ffc0337/apiKeys/b95d049e-dea7-4385-99f6-a67a96e7b717"
        url = "https://api.commerce.coinbase.com/charges"
        api_key = COINBASE_API_KEY

        payload = {
            "name": f"Buy {crypto}",
            "description": f"Purchase {crypto} and send to wallet {wallet_address}",
            "pricing_type": "fixed_price",
            "local_price": {"amount": str(amount), "currency": currency},
            "metadata": {
                "user_id": request.user.id,
                "crypto": crypto,
                "wallet_address": wallet_address,
            },
        }

        headers = {
            "X-CC-Api-Key": api_key,
            "X-CC-Version": "2018-03-22",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers, timeout=20)
        # forward success payload
        if response.status_code in (200, 201):
            data = response.json()
            hosted = data.get("data", {}).get("hosted_url")
            charge_id = data.get("data", {}).get("id")
            return Response({
                "redirect_url": hosted,
                "charge_id": charge_id,
                "raw": data
            }, status=status.HTTP_200_OK)

        # try to parse error and return it so frontend can show reason
        try:
            err = response.json()
        except Exception:
            err = {"status_code": response.status_code, "text": response.text}
        logger.error("Coinbase charge failed: %s", err)
        return Response({"error": "Failed to create Coinbase charge", "details": err},
                        status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.exception("coinbase_start error")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Kraken
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def kraken_start(request):
    try:
        amount = request.data.get("amount")
        crypto = request.data.get("crypto")
        wallet_address = request.data.get("wallet_address")

        if not all([amount, crypto, wallet_address]):
            return Response(
                {"error": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # For Kraken, redirect to their website with parameters
        kraken_url = f"https://www.kraken.com/sign-up?referralid=YOURREFERRALID"
        
        return Response({
            "redirect_url": kraken_url,
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Binance
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def binance_start(request):
    try:
        amount = request.data.get("amount")
        crypto = request.data.get("crypto")
        wallet_address = request.data.get("wallet_address")

        if not all([amount, crypto, wallet_address]):
            return Response(
                {"error": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # For Binance, redirect to their fiat gateway
        binance_url = "https://www.binance.com/en/buy-sell/crypto"
        
        return Response({
            "redirect_url": binance_url,
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Gemini
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def gemini_start(request):
    try:
        amount = request.data.get("amount")
        crypto = request.data.get("crypto")
        wallet_address = request.data.get("wallet_address")

        if not all([amount, crypto, wallet_address]):
            return Response(
                {"error": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # For Gemini, redirect to their platform
        gemini_url = "https://www.gemini.com/"
        
        return Response({
            "redirect_url": gemini_url,
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Ramp
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ramp_start(request):
    try:
        crypto = request.data.get("crypto")
        wallet_address = request.data.get("wallet_address")
        amount = request.data.get("amount")

        if not all([crypto, wallet_address]):
            return Response(
                {"error": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ramp API
        ramp_url = f"https://buy.ramp.network/?userAddress={wallet_address}&fiatCurrency=USD&fiatValue={amount}"
        
        return Response({
            "redirect_url": ramp_url,
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Crypto.com
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def crypto_com_start(request):
    try:
        amount = request.data.get("amount")
        crypto = request.data.get("crypto")
        wallet_address = request.data.get("wallet_address")

        if not all([amount, crypto, wallet_address]):
            return Response(
                {"error": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crypto.com platform
        crypto_com_url = "https://crypto.com/en/exchange/buy-sell"
        
        return Response({
            "redirect_url": crypto_com_url,
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )