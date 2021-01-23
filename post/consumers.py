from post.models import Comment, Post
import json
import datetime as dt

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.me = self.scope['user']
        print(self.me)
        self.room_name = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = 'comment_%s' % self.room_name
        print(self.room_name)
        print(self.room_group_name)
        print(self.channel_name)
        print(self.channel_layer)

        # Get post database to save comment
        self.post = await database_sync_to_async(
            Post.objects.get)(id=self.room_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive comment from WebSocket
    # This is what received when user click enter to post a comment on page
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        comment = text_data_json['comment']
        print(comment)

        # Save comments to database
        comment_obj = Comment(
            commentor=self.me,
            post=self.post,
            content=comment,
            written=dt.datetime.now,
            modified=dt.datetime.now
        )

        await database_sync_to_async(comment_obj.save)()

        # Send comment to room group
        # These are what will be sent to the post_comment function below
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'post_comment',
                'comment': comment,
                'commentor_id': comment_obj.commentor.id,
                'commentor_name': comment_obj.commentor.username,
            }
        )
    
    # Receive comment from room group
    async def post_comment(self, event):
        comment = event['comment']
        commentor_id = event['commentor_id']
        commentor_name = event['commentor_name']

        # Send comment to WebSocket
        # These are what HTML file will receive
        await self.send(text_data=json.dumps({
            'comment': comment,
            'commentor_id': commentor_id,
            'commentor_name': commentor_name,
        }))
