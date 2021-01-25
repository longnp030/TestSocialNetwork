from user.models import User
from post.models import Comment, Post, Reaction
from django.shortcuts import redirect, render
from django.urls import reverse

from chat.views import get_available_chats as gac
# Create your views here.

def like_post(request, post_id):
    if len(Reaction.objects.filter(post=Post.objects.get(id=post_id), liker=User.objects.get(id=request.user.id))) > 0:
        return redirect(reverse('post:post_view', kwargs={'post_id': post_id}))
    Reaction.objects.create(
        post=Post.objects.get(id=post_id),
        liker=User.objects.get(id=request.user.id)
    )
    return redirect(reverse('post:post_view', kwargs={'post_id': post_id}))

def unlike_post(request, post_id):
    try:
        Reaction.objects.get(
            post=Post.objects.get(id=post_id),
            liker=User.objects.get(id=request.user.id)
        ).delete()
    except Exception as e:
        return redirect(reverse('post:post_view', kwargs={'post_id': post_id}))
    else:
        return redirect(reverse('post:post_view', kwargs={'post_id': post_id}))

def post_view(request, post_id):
    me = User.objects.filter(id=request.user.id).first()
    post = Post.objects.get(id=post_id)
    reactions = Reaction.objects.filter(post=post)
    liked = len(reactions.filter(liker=me)) > 0
    comments = Comment.objects.filter(post=post)

    context = {
        'post_id': post_id,
        'me': me,
        'post': post,
        'liked': liked,
        'reactions': reactions,
        'comments': comments,
        'view': 'post',
        'personnal_chats': gac(request)['personnal_chats'],
        'group_chats': gac(request)['group_chats'],
    }
    return render(request, 'post/post_view.html', context)

def delete(request, post_id):
    Post.objects.get(id=post_id).delete()
    return redirect('home')

def edit(request, post_id):
    pass
