from django.urls import path
from .consumers import TaskNotificationConsumer

websocket_urlpatterns=[
    path('ws/notification-to-technicians/', TaskNotificationConsumer.as_asgi())
]