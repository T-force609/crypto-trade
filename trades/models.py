from django.db import models
from django.conf import settings
from market.models import CryptoAsset
from django.contrib.auth.models import User
import uuid

def generate_wallet_address():
    return uuid.uuid4().hex[:32]
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    address = models.CharField(max_length=255, unique=True, editable=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.address:
            self.address = f"0x{uuid.uuid4().hex[:32]}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username}'s Wallet({self.address})"

class Holding(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='holdings')
    asset = models.ForeignKey(CryptoAsset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=30, decimal_places=16, default=0)
    avg_price = models.DecimalField(max_digits=30, decimal_places=8, default=0)

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    asset = models.ForeignKey(CryptoAsset, on_delete=models.CASCADE, null=True, blank=True)
    tx_type = models.CharField(max_length=4, choices=(('BUY','BUY'),('SELL','SELL')))
    quantity = models.DecimalField(max_digits=30, decimal_places=16)
    price_per_unit = models.DecimalField(max_digits=30, decimal_places=8)
    total = models.DecimalField(max_digits=30, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return self.quantity * self.price_per_unit

    def __str__(self):
        return f"{self.tx_type} {self.quantity} {self.asset.symbol}"

class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deposits")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="deposits")
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=10, default="USDT")
    tx_hash = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deposit {self.amount} {self.currency} by {self.user.username}"
