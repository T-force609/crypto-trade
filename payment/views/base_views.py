from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from payment.models import PaymentTransaction

def create_transaction(user, provider, amount, currency="USD"):
    tx = PaymentTransaction.objects.create(
        user=user,
        provider=provider,
        amount=amount,
        currency=currency,
        status="pending"
    )
    return tx

def success_response(data):
    return Response({"success": True, **data}, status=status.HTTP_200_OK)

def error_response(message):
    return Response({"success": False, "error": message}, status=status.HTTP_400_BAD_REQUEST)
