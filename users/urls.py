from django.urls import path
from .views import RegisterView, CountryListView, AdminTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('admin_site/', AdminTokenObtainPairView.as_view(), name="admin_token_obtain_pair"),
]
