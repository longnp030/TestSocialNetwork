import json
from django.db.models.query_utils import Q
from chat.models import ChatBox, GroupChatBox, GroupMessage, JoinGroupChat, Message
from django.shortcuts import redirect, render
from django.urls import reverse

from user.models import *
from .forms import *

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
        'personnal_chats': get_available_chats(request)['personnal_chats'],
        'group_chats': get_available_chats(request)['group_chats'],
        'data': json.dumps(contextDict)
    }
    return render(request, 'chat/room.html', context)

def is_member_of_group_chat(request, group_chat_id):
    return len(GroupChatBox.objects.filter(creator=request.user)) > 0 or len(JoinGroupChat.objects.filter(groupchatbox=GroupChatBox.objects.get(id=group_chat_id), invitee=request.user)) > 0

def group_room(request, group_chat_id):
    if not is_member_of_group_chat(request, group_chat_id):
        return redirect('home')
    me = User.objects.get(id=request.user.id)
    groupchatbox = GroupChatBox.objects.filter(
        id=group_chat_id
    )
    if len(groupchatbox) == 0:
        groupchatbox = GroupChatBox.objects.create(creator=me)
    else:
        groupchatbox = groupchatbox[0]
    try:
        groupmessages = list(GroupMessage.objects.filter(chatbox=groupchatbox))
    except:
        groupmessages = []
    try:
        me_avatar = me.avatar.url
    except:
        me_avatar = None

    if request.method == 'POST':
        groupchataddmemberform = GroupChatAddMemberForm(request.POST, initial={'inviter': me, 'groupchatbox':groupchatbox})
        if groupchataddmemberform.is_valid():
            print('add form')
            print(groupchataddmemberform.cleaned_data['invitee'], type(groupchataddmemberform.cleaned_data['invitee']))
            groupchataddmemberform.save()
            return redirect(reverse('chat:group_room', kwargs={'group_chat_id': group_chat_id}))
        return redirect(reverse('chat:group_room', kwargs={'group_chat_id': group_chat_id}))
    else:
        groupchataddmemberform = GroupChatAddMemberForm(initial={'inviter': me, 'groupchatbox':groupchatbox})

    if request.method == 'POST':
        changechatnameform = ChangeChatNameForm(request.POST, instance=GroupChatBox.objects.get(id=group_chat_id))
        if changechatnameform.is_valid():
            changechatnameform.save()
            return redirect(reverse('chat:group_room', kwargs={'group_chat_id': group_chat_id}))
        return redirect(reverse('chat:group_room', kwargs={'group_chat_id': group_chat_id}))
    else:
        changechatnameform = ChangeChatNameForm(instance=GroupChatBox.objects.get(id=group_chat_id))
        
    contextDict = {
        'me_id': me.id,
        'me_name': me.username,
        'me_avatar': me_avatar,
        'groupchatbox_name': groupchatbox.name,
        'groupmessages': json.dumps([{
            'groupmessage_sender_id': groupmessage.sender.id,
            'groupmessage_sender_name': groupmessage.sender.username,
            #'message_sender_avatar': None if message.sender.avatar is None else message.sender.avatar.url,
            'groupmessage_content': groupmessage.content,
            'groupmessage_sent': str(groupmessage.sent),
        } for groupmessage in groupmessages]),
    }
    context = {
        'personnal_chats': get_available_chats(request)['personnal_chats'],
        'group_chats': get_available_chats(request)['group_chats'],
        'groupchataddmemberform': groupchataddmemberform,
        'changechatnameform': changechatnameform,
        'me': me,
        'groupchatbox': groupchatbox,
        'group_chat_id': group_chat_id,
        'group_chat_name': groupchatbox.name,
        'groupchat_member': [GroupChatBox.objects.get(id=group_chat_id).creator] + [join.invitee for join in JoinGroupChat.objects.filter(groupchatbox=GroupChatBox.objects.get(id=group_chat_id))],
        'groupchatbox_creator': GroupChatBox.objects.get(id=group_chat_id).creator,
        'is_creator': me == GroupChatBox.objects.get(id=group_chat_id).creator,
        'data': json.dumps(contextDict)
    }
    return render(request, 'chat/group_room.html', context)

def create_group_chat(request, creator_id):
    groupchatbox = GroupChatBox.objects.create(creator=User.objects.get(id=creator_id))
    return redirect(reverse('chat:group_room', kwargs={'group_chat_id': groupchatbox.id}))

def add_member(request, group_chat_id):
    if not is_member_of_group_chat(request, group_chat_id):
        return redirect('home')
    if request.method == 'POST':
        form = GroupChatAddMemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('chat:group_room', kwargs={'group_chat_id': group_chat_id}))
    else:
        form = GroupChatAddMemberForm()
    context = {
        'form': form,
    }
    return render(request, 'chat/add_member.html', context)

def change_chat_name(request, group_chat_id):
    if not is_member_of_group_chat(request, group_chat_id):
        return redirect('home')
    if request.method == 'POST':
        form = ChangeChatNameForm(request.POST, instance=GroupChatBox.objects.get(id=group_chat_id))
        if form.is_valid():
            form.save()
            return redirect(reverse('chat:group_room', kwargs={'group_chat_id': group_chat_id}))
    else:
        form = ChangeChatNameForm(instance=GroupChatBox.objects.get(id=group_chat_id))
    context = {
        'form': form,
    }
    return render(request, 'chat/change_chat_name.html', context)

def get_available_chats(request):
    me = User.objects.get(id=request.user.id)
    personnal_chats = ChatBox.objects.filter(Q(user1=me)|Q(user2=me))
    group_chats = list(GroupChatBox.objects.filter(creator=me)) + [join.groupchatbox for join in JoinGroupChat.objects.filter(invitee=me)]

    return {
        'personnal_chats': [{
            'chat': chat,
            'receiver_id': chat.user2.id if chat.user1 == me else chat.user1.id,
        } for chat in personnal_chats],
        'group_chats': group_chats,
    }

def kick(request, group_chat_id, member_id):
    JoinGroupChat.objects.get(groupchatbox=GroupChatBox.objects.get(id=group_chat_id), invitee=User.objects.get(id=member_id)).delete()
    return redirect(reverse('chat:group_room', kwargs={'group_chat_id': group_chat_id}))

def leave(request, group_chat_id):
    JoinGroupChat.objects.get(groupchatbox=GroupChatBox.objects.get(id=group_chat_id), invitee=User.objects.get(id=request.user.id)).delete()
    return redirect(reverse('chat:group_room', kwargs={'group_chat_id': group_chat_id}))
