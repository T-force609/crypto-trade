from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class PaymentTransaction(models.Model):
    PROVIDERS = [
        ("coinbase", "Coinbase"),
        ("ramp", "Ramp"),
        ("transak", "Transak"),
        ("crypto_com", "Crypto.com"),
        ("bybit", "Bybit"),
        ("gemini", "Gemini"),
        ("kraken", "Kraken"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.CharField(max_length=50, choices=PROVIDERS)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    tx_hash = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.provider} - {self.status}"
