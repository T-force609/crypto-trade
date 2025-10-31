from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from .models import Wallet, Holding, Transaction
from market.models import CryptoAsset
from decimal import Decimal
from rest_framework import generics
from .serializers import WalletSerializer, TransactionSerializer
from .models import Deposit, Wallet
from .serializers import DepositSerializer
from rest_framework.decorators import api_view

class TradeView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """
        expected body:
        { "symbol": "BTC", "tx_type": "BUY", "quantity": "0.01", "price_per_unit": "45000" }
        """
        user = request.user
        wallet = Wallet.objects.get(user=user)
        symbol = request.data.get("symbol")
        tx_type = request.data.get("tx_type")  # BUY or SELL
        qty = Decimal(request.data.get("quantity"))
        price = Decimal(request.data.get("price_per_unit"))
        total = qty * price

        asset = CryptoAsset.objects.filter(symbol__iexact=symbol).first()
        if not asset:
            return Response({"detail":"Asset not found"}, status=status.HTTP_400_BAD_REQUEST)

        if tx_type == "BUY":
            # check fiat balance
            if wallet.balance < total:
                return Response({"detail":"Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
            # deduct fiat
            wallet.balance -= total
            wallet.save()
            # update holdings
            holding, _ = Holding.objects.get_or_create(wallet=wallet, asset=asset)
            # new avg price calculation
            new_total_qty = holding.quantity + qty
            if holding.quantity == 0:
                holding.avg_price = price
            else:
                holding.avg_price = ((holding.avg_price * holding.quantity) + (price * qty)) / new_total_qty
            holding.quantity = new_total_qty
            holding.save()
            tx = Transaction.objects.create(wallet=wallet, asset=asset, tx_type="BUY",
                    quantity=qty, price_per_unit=price, total=total)
            return Response({"detail":"Bought", "transaction_id": tx.id})

        elif tx_type == "SELL":
            holding = Holding.objects.filter(wallet=wallet, asset=asset).first()
            if not holding or holding.quantity < qty:
                return Response({"detail":"Insufficient asset quantity"}, status=status.HTTP_400_BAD_REQUEST)
            # reduce holding
            holding.quantity -= qty
            holding.save()
            # credit fiat
            wallet.balance += total
            wallet.save()
            tx = Transaction.objects.create(wallet=wallet, asset=asset, tx_type="SELL",
                    quantity=qty, price_per_unit=price, total=total)
            return Response({"detail":"Sold", "transaction_id": tx.id})
        else:
            return Response({"detail":"Invalid tx_type"}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class PortfolioView(APIView):
    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        holdings = wallet.holdings.all()
        holdings_data = [
            {
                "asset": h.asset.symbol,
                "quantity": h.quantity,
                "avg_price": h.avg_price
            } for h in holdings
        ]
        data = {
            "balance": wallet.balance,
            "address": wallet.address,
            "holdings": holdings_data,
        }
        return Response(data)

    

class TransactionListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        transactions = wallet.transactions.order_by("-timestamp")
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    

class DepositCreateAPIView(generics.CreateAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        wallet = self.request.user.wallet
        deposit = serializer.save(user=self.request.user, wallet=wallet)
        wallet.balance += deposit.amount
        wallet.save()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_deposit(request):
    serializer = DepositSerializer(data=request.data)
    if serializer.is_valid():
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        deposit = serializer.save(user=request.user, wallet=wallet)
        return Response(
            {"message": "Deposit created successfully", "deposit_id": deposit.id},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def deposit_funds(request):
    """
    Simulate deposit of funds (to admin wallet but credited to user).
    Expected body:
    {
        "amount": "500.00"
    }
    """
    try:
        amount = Decimal(request.data.get("amount", 0))
        if amount <= 0:
            return Response({"detail": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)

        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        wallet.balance += amount
        wallet.save()

        return Response({
            "detail": f"Deposit of ${amount} successful.",
            "new_balance": wallet.balance
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_wallet_address(request):
    user = request.user
    address = request.data.get("address")

    if not address:
        return Response({"error": "Address required"}, status=status.HTTP_400_BAD_REQUEST)

    wallet, created = Wallet.objects.get_or_create(user=user)
    wallet.address = address
    wallet.save()

    return Response({"message": "Wallet address saved successfully", "address": address})

@permission_classes([IsAuthenticated])
class DepositView(APIView):
    def post(self, request):
        coin = request.data.get("coin")
        amount = request.data.get("amount")
        wallet_address = request.data.get("wallet_address")

        deposit = Deposit.objects.create(
            user=request.user,
            coin=coin,
            amount=amount,
            wallet_address=wallet_address
        )
        return Response({"detail": "Deposit request created", "id": deposit.id})
    


@api_view(["GET"])
@permission_classes([AllowAny])
def get_admin_wallet(request):
    """Return admin user's wallet address."""
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        wallet = Wallet.objects.get(user=admin_user)
        return Response({"address": wallet.address})
    except Wallet.DoesNotExist:
        return Response({"detail": "Admin wallet not found"}, status=404)