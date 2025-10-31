from rest_framework import serializers
from .models import Wallet, Holding, Transaction
from .models import Deposit

from rest_framework import serializers
from .models import Deposit
from market.models import CryptoAsset

class DepositSerializer(serializers.ModelSerializer):
    coin_id = serializers.PrimaryKeyRelatedField(
        queryset=CryptoAsset.objects.all(),
        source='asset',
        write_only=True
    )

    class Meta:
        model = Deposit
        fields = ['id', 'user', 'coin_id', 'amount', 'currency', 'timestamp', 'wallet']
        read_only_fields = ['id', 'timestamp']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class HoldingSerializer(serializers.ModelSerializer):
    asset = serializers.StringRelatedField()
    class Meta:
        model = Holding
        fields = ('asset','quantity','avg_price')

class WalletSerializer(serializers.ModelSerializer):
    holdings = HoldingSerializer(many=True, read_only=True)
    class Meta:
        model = Wallet
        fields = ('id', 'balance','holdings', 'address', 'user')
