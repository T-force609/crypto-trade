from django.urls import path
from payment.views import coinbase_views, transak_views

urlpatterns = [
    path("coinbase/start/", coinbase_views.start_coinbase_payment, name="coinbase_start"),
    path("transak/start/", transak_views.start_transak_payment, name="transak_start"),
]
