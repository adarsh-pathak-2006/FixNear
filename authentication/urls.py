from django.urls import path
from .views import (
    CustomTokenObtainView,
    CustomTokenRefreshView,
    RegisterAPI,
    MyCustomerProfile,
    MyTechnicianProfile,
    TechnicianProfileListAPI,
)

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='auth-register'),
    path('token/', CustomTokenObtainView.as_view(), name='auth-token-obtain'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='auth-token-refresh'),
    path('my-profile/', MyCustomerProfile.as_view(), name='auth-my-customer-profile'),
    path('my-technician-profile/', MyTechnicianProfile.as_view(), name='auth-my-technician-profile'),
    path('technicians/', TechnicianProfileListAPI.as_view(), name='auth-technician-list'),
]