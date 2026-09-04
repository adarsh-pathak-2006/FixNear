from django.urls import path
from .views import AllRequestListAPI, RepairRequestAcceptAPI, RepairStatusUpdateAPI

urlpatterns = [
    path('all-request/', AllRequestListAPI.as_view(), name='technician-all-requests'),
    path('request/<int:pk>/', RepairRequestAcceptAPI.as_view(), name='technician-request-detail'),
    path('status/<int:pk>/', RepairStatusUpdateAPI.as_view(), name='technician-repair-status'),
]