from rest_framework import serializers
from .models import CryptoAsset

class CryptoAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoAsset
        fields = '__all__'
