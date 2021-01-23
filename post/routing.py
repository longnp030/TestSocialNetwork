# post/routing.py
from django.urls.conf import path

from . import consumers

websocket_urlpatterns = [
    path('ws/post/<slug:post_id>/', consumers.CommentConsumer.as_asgi()),
]