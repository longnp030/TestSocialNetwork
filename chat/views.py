import json
from django.db.models.query_utils import Q
from chat.models import ChatBox, Message
from django.shortcuts import render

from user.models import *

# Create your views here.

def room(request, user_id):
    me = User.objects.get(id=request.user.id)
    receiver = User.objects.get(id=user_id)
    chatbox = ChatBox.objects.filter(
        Q(user1=me)|Q(user2=me)).filter(
        Q(user1=receiver)|Q(user2=receiver))
    if len(chatbox) == 0:
        chatbox = ChatBox(user1=me, user2=receiver)
        chatbox.save()
    else:
        chatbox = chatbox[0]
    try:
        messages = list(Message.objects.filter(chatbox=chatbox))
    except Exception as e:
        messages = []
    try:
        me_avatar = me.avatar.url
    except Exception as e:
        me_avatar = None
    try:
        receiver_avatar = receiver.avatar.url
    except Exception as e:
        receiver_avatar = None
    contextDict = {
        'me_id': me.id,
        'me_name': me.username,
        'me_avatar': me_avatar,
        'receiver_id': receiver.id,
        'receiver_name': receiver.username,
        'receiver_avatar': receiver_avatar,
        'chatbox_name': chatbox.name,
        'messages': json.dumps([{
            'message_sender_id': message.sender.id,
            'message_sender_name': message.sender.username,
            #'message_sender_avatar': None if message.sender.avatar is None else message.sender.avatar.url,
            'message_receiver_id': message.receiver.id,
            'message_receiver_name': message.receiver.username,
            #'message_receiver_avatar': None if message.receiver.avatar is None else message.receiver.avatar,
            'message_content': message.content,
            'message_sent': str(message.sent),
        } for message in messages]),
    }
    context = {
        'user_id': user_id,
        'data': json.dumps(contextDict)
    }
    return render(request, 'chat/room.html', context)
   