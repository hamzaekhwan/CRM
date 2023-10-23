
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from CRMapp.models import Reminder
from asgiref.sync import async_to_sync
from datetime import datetime
from django.contrib.auth.models import User

class ReminderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def notify(self, event):
        await self.send(event["text"])

    @database_sync_to_async
    def send_notification(self, reminder):
        users=User.objects.all()
        for user in users:
            async_to_sync(self.channel_layer.group_send)(
                str(user.pk),
                {
                    "type": "notify",
                    "text": reminder.message,
                },
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["action"] == "start":
            current_time = datetime.now()
            reminders = Reminder.objects.filter(
                reminder_datetime__lte=current_time,
                notification_sent=False

            )

            for reminder in reminders:
                await self.send_notification(reminder)

                reminder.notification_sent = True
                reminder.save()
