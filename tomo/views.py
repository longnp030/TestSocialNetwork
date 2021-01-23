from django.db.models.query_utils import Q
from user.models import *
from post.models import *
from post.forms import *
from django.shortcuts import redirect, render


def home(request):
    me = None if request.user is None else User.objects.get(id=request.user.id)

    if request.method == 'POST':
        post_create_form = PostCreationForm(
            request.POST, request.FILES,
        )
        if post_create_form.is_valid():
            post = post_create_form.save(commit=False)
            post.author = me
            post.save()
            return redirect('home')
    else:
        post_create_form = PostCreationForm()
    
    '''my_posts = Post.objects.filter(author=me)
    my_friendships1 = Friendship.objects.filter(user1=me)
    my_friendships2 = Friendship.objects.filter(user2=me)
    friends = []
    for my_friendship in my_friendships1:
        friends.append(User.objects.get(id=my_friendship.user2.id))
    for my_friendship in my_friendships2:
        friends.append(User.objects.get(id=my_friendship.user1.id))
    friends_posts = []
    for friend in friends:
        friends_posts = Post.objects.filter(author=friend)
    friends_posts = [friend_posts for friend_posts in friends_posts]'''
    posts = Post.objects.all()
    context = {
        'form': post_create_form,
        'posts': [{
            'post': post,
            'reactions': None if len(Reaction.objects.filter(post=post)) == 0 else Reaction.objects.filter(post=post)[0],
            'comments': Comment.objects.filter(post=post),
        } for post in posts],
    }
    return render(request, 'home.html', context)