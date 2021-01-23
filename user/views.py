from django.template.defaulttags import register
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
import datetime as dt

from .models import *
from .forms import *

# Create your views here.


class CreateUserView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        valid = super(CreateUserView, self).form_valid(form)
        username, password = form.cleaned_data.get(
            'username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


def user_profile(request, user_id):
    viewing_user = User.objects.get(id=user_id)
    me = User.objects.get(id=request.user.id)

    mine = me == viewing_user

    form = None
    is_friend = False
    friend_request_sended = False
    received_friend_requests = None
    friends = None
    if mine:
        received_friend_requests = FriendRequest.objects.filter(receiver=me)
        friends = []
        for my_friendship in Friendship.objects.filter(user1=me):
            friends.append(User.objects.get(id=my_friendship.user2.id))
        for my_friendship in Friendship.objects.filter(user2=me):
            friends.append(User.objects.get(id=my_friendship.user1.id))
        if request.method == 'POST':
            form = ProfileChangeForm(request.POST, request.FILES)
            if form.is_valid():
                me.avatar = request.FILES.get('avatar') if request.FILES.get(
                    'avatar') is not None else me.avatar
                me.save()
                return redirect(reverse('user:user_profile', kwargs={'user_id': me.id}))
            else:
                form = ProfileChangeForm()
    else:
        is_friend = len(
            Friendship.objects.filter(
                Q(user1=me) | Q(user1=viewing_user)
            ).filter(
                Q(user2=me) | Q(user2=viewing_user)
            )) > 0
        friend_request_sended = len(FriendRequest.objects.filter(
            sender=me, receiver=viewing_user)) > 0

    context = {
        'me': me,
        'viewing_user': viewing_user,
        'mine': mine,
        'form': form,
        'is_friend': is_friend,
        'friend_request_sended': friend_request_sended,
        'received_friend_requests': received_friend_requests,
        'friends': friends,
    }
    return render(request, 'user_profile.html', context)


def send_friend_request(request, user_id):
    me = User.objects.get(id=request.user.id)
    receiver = User.objects.get(id=user_id)
    friend_request = FriendRequest(
        sender=me, receiver=receiver,
        sended=dt.datetime.now,
        status=0)
    friend_request.save()
    return redirect(reverse('user:user_profile', kwargs={'user_id': user_id}))


def cancel_friend_request(request, user_id):
    me = User.objects.get(id=request.user.id)
    receiver = User.objects.get(id=user_id)
    friend_request = None
    try:
        friend_request = FriendRequest.objects.get(sender=me, receiver=receiver)
    except Exception as e:
        return redirect(reverse('user:user_profile', kwargs={'user_id': user_id}))
    else:
        friend_request.delete()
    return redirect(reverse('user:user_profile', kwargs={'user_id': user_id}))


def accept_friend_request(request, user_id):
    me = User.objects.get(id=request.user.id)
    sender = User.objects.get(id=user_id)
    friendship = Friendship(user1=sender, user2=me, added=dt.datetime.now)
    friendship.save()
    friend_request = FriendRequest.objects.get(sender=sender, receiver=me)
    friend_request.delete()
    return redirect(reverse('user:user_profile', kwargs={'user_id': me.id}))


def reject_friend_request(request, user_id):
    me = User.objects.get(id=request.user.id)
    sender = User.objects.get(id=user_id)
    friend_request = FriendRequest.objects.get(sender=sender, receiver=me)
    friend_request.delete()
    return redirect(reverse('user:user_profile', kwargs={'user_id': me.id}))


def unfriend(request, user_id):
    me = User.objects.get(id=request.user.id)
    friend = User.objects.get(id=user_id)
    friendship = None
    if len(Friendship.objects.filter(user1=me, user2=friend)) > 0:
        friendship = Friendship.objects.get(user1=me, user2=friend)
    else:
        friendship = Friendship.objects.get(user1=friend, user2=me)
    friendship.delete()
    return redirect(reverse('user:user_profile', kwargs={'user_id': user_id}))
