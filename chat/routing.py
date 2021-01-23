# chat/routing.py
from django.urls.conf import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<slug:user_id>/', consumers.ChatConsumer.as_asgi()),
]