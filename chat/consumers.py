# chat/consumers.py
from django.db.models.query_utils import Q
from chat.models import ChatBox, Message
import json
import datetime as dt

from channels.db import database_sync_to_async
from user.models import User
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.me = self.scope['user']
        self.friend = await database_sync_to_async(
            User.objects.get
        )(id=self.scope['url_route']['kwargs']['user_id'])  # get(id=self.scope['url_route']['kwargs']['user_id'])
        print(self.me)
        print(self.friend)
        self.room_name = await self.get_room_name()
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_name)
        print(self.room_group_name)
        print(self.channel_name)
        print(self.channel_layer)

        # Get database box to save chat status
        self.chatbox = await database_sync_to_async(
            ChatBox.objects.get)(name=self.room_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def get_room_name(self):
        return ChatBox.objects.get(
                (Q(user1=self.me)|Q(user2=self.me))&(Q(user1=self.friend)|Q(user2=self.friend))
            ).name

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']
        print(message)

        # Save messages to database
        message_obj = Message(
            sender=self.me, receiver=self.friend,
            content=message,
            chatbox=self.chatbox,
            sent=dt.datetime.now
        )
        await database_sync_to_async(message_obj.save)()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        print(message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))