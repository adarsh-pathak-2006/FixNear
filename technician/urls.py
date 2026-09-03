from django.urls import path
from .views import AllRequestListAPI, RepairRequestAcceptAPI, RepairStatusUpdateAPI


urlpatterns=[
    path('all-request/', AllRequestListAPI.as_view()),
    path('request/<int:pk>/', RepairRequestAcceptAPI.as_view()),
    path('status/<int:pk>/', RepairStatusUpdateAPI.as_view()),
]