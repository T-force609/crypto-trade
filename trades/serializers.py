from rest_framework import serializers
from .models import Wallet, Holding, Transaction

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
        fields = ('id','balance','holdings')
