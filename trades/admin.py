from django.contrib import admin
from .models import Wallet, Transaction, Holding

# Register your models here.

admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Holding)