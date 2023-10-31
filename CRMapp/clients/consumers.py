from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async

from channels.layers import get_channel_layer
from CRMapp.models import *
from django.contrib.auth.models import User,AnonymousUser


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except:
        return AnonymousUser()

@database_sync_to_async
def create_reminder(receiver):
    reminder_to_create=Reminder.objects.create(admin=receiver)
    print('I am here to help')
    return (reminder_to_create.admin.username)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
            print('connected')
            print('Am i finallyy here')
       
            await self.accept()

            await self.send(json.dumps({
                        "type":"websocket.send",
                        "text":"hello world"
                    }))
  
            self.send({
                "type":"websocket.send",
                "text":"room made"
            })
    
    async def disconnect(self):
        print('disconnect')
        
    async def receive(self,event):
        print(event)
        data_to_get=json.loads(event['text'])
        user_to_get=await get_user(int(data_to_get))
        print(user_to_get)
        get_of=await create_reminder(user_to_get)
        self.room_group_name='test_consumer_group'
        channel_layer=get_channel_layer()
        await (channel_layer.group_send)(
            self.room_group_name,
            {
                "type":"send_notification",
                "value":json.dumps(get_of)
            }
)
        print('receive',event)        

    
    async def send_notification(self,event):
        await self.send(json.dumps({
            "type":"websocket.send",
            "data":event
        }))
        print('I am here')
        print(event)    

