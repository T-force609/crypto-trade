from django.urls import path
from .views import contact_support

urlpatterns = [
    path("contact/", contact_support, name="contact_support"),
]
