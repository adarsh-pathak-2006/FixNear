from django.urls import path
from .views import CustomTokenObtainView, CustomTokenRefreshView, RegisterAPI, MyCustomerProfile, MyTechnicianProfile, TechnicalProfileListAPI

urlpatterns=[
    path('register/', RegisterAPI.as_view()),
    path('token/', CustomTokenObtainView.as_view()),
    path('token/refresh/', CustomTokenRefreshView.as_view()),
    path('my-profile/', MyCustomerProfile.as_view()),
    path('my-technician-profile/', MyTechnicianProfile.as_view()),
    path('technicians/', TechnicalProfileListAPI.as_view()),
]