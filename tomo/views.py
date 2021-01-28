from chat.models import *
from django.db.models.query_utils import Q
from user.models import *
from post.models import *
from post.forms import *
from django.shortcuts import render
from chat.views import get_available_chats as gac

def home(request):
    me = None if request.user.id is None else User.objects.get(id=request.user.id)
    
    personnal_chats = ChatBox.objects.filter(Q(user1=me)|Q(user2=me))
    group_chats = list(GroupChatBox.objects.filter(creator=me)) + [join.groupchatbox for join in JoinGroupChat.objects.filter(invitee=me)]

    posts = Post.objects.all()
    context = {
        'posts': [{
            'post': post,
            'reactions': Reaction.objects.filter(post=post),
            'liked': len(Reaction.objects.filter(post=post, liker=me)) > 0,
            'comments': Comment.objects.filter(post=post),
        } for post in reversed(posts)],
        'me': me,
        'personnal_chats': [{
            'chat': chat,
            'receiver_id': chat.user2.id if chat.user1 == me else chat.user1.id,
        } for chat in personnal_chats],
        'group_chats': group_chats,
        'view': 'home',
    }
    return render(request, 'home.html', context)
