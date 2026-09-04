from django.urls import path
from .views import RepairRequestAPI

urlpatterns = [
    path('repair-request/', RepairRequestAPI.as_view(), name='customer-repair-request'),
]