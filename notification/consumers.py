# notification/consumers.py
from notification.models import *
from user.models import *
from post.models import *

import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.me = self.scope['user']
        self.room_group_name = 'home'

        await  self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
