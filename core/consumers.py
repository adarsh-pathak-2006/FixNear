from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
from technician.models import SentRequest
from .models import NotificationLog
from authentication.models import TechnicianProfile
import json

class TaskNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user=self.scope['user']
        if self.user.is_authenticated and await SentRequest.objects.select_related('technician__user').filter(technician__user=self.user).aexists():
            self.group_name="RepairRequestNotification"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def receive(self, text_data):
        db_data=await SentRequest.objects.select_related('technician__user').aget(technician__user=self.user)
        message_skill=db_data.request.skills_required
        message_requirement=db_data.request.requirement
        tech_profile_data=await TechnicianProfile.objects.select_related('user').aget(user=self.user)
        await NotificationLog.objects.acreate(technician=tech_profile_data, skill_required=message_skill, requirement=message_requirement)
        await self.channel_layer.group_send(self.group_name, {'type':'notification', 'notification_skill_required':message_skill, 'notification_requirement':message_requirement})

    async def notification(self, event):
        await self.send(text_data=json.dumps({'notification_skill_required':event['notification_skill_required'], 'notification_requirement':event.get('notification_requirement')}))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
