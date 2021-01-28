from post.forms import *
from user.models import *
from post.models import *
from django.shortcuts import redirect, render
from django.urls import reverse

from chat.views import get_available_chats as gac
# Create your views here.

def create_post(request):
    me = None if request.user.id is None else User.objects.get(id=request.user.id)
    if request.method == 'POST':
        post_create_form = PostCreationForm(request.POST, request.FILES)
        if post_create_form.is_valid():
            post = post_create_form.save(commit=False)
            post.author = me
            post.save()
            return redirect(reverse('post:add_img', kwargs={'post_id': post.id}))
    else:
        post_create_form = PostCreationForm()
    context = {
        'me': me,
        'form': post_create_form,
        'personnal_chats': gac(request)['personnal_chats'],
        'group_chats': gac(request)['group_chats'],
    }
    return render(request, 'post/create.html', context)

def add_img(request, post_id):
    me = None if request.user.id is None else User.objects.get(id=request.user.id)
    post = Post.objects.get(id=post_id)
    this_post_imgs = Image.objects.order_by('uploaded')

    if request.method == 'POST':
        upload_img_form = ImageUploadForm(request.POST, request.FILES)
        if upload_img_form.is_valid():
            img = upload_img_form.save(commit=False)
            img.author = me
            img.save()
            return redirect(reverse('post:add_img', kwargs={'post_id': post_id}))
    else:
        upload_img_form = ImageUploadForm()

    if request.method == 'POST':
        add_img_form = PostAddImageForm(request.POST, instance=post)
        if add_img_form.is_valid():
            add_img_form.save()
            return redirect('home')
    else:
        add_img_form = PostAddImageForm(instance=post)
    context = {
        'add_form': add_img_form,
        'upload_form': upload_img_form,
        'personnal_chats': gac(request)['personnal_chats'],
        'group_chats': gac(request)['group_chats'],
        'this_post_imgs': this_post_imgs,
    }
    return render(request, 'post/add_img.html', context)

def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        edit_post_form = PostEditForm(request.POST, instance=post)
        if edit_post_form.is_valid():
            edit_post_form.save()
            return redirect(reverse('post:post_view', kwargs={'post_id': post_id}))
    else:
        edit_post_form = PostEditForm(instance=post)
    context = {
        'form': edit_post_form,
        'personnal_chats': gac(request)['personnal_chats'],
        'group_chats': gac(request)['group_chats'],
    }
    return render(request, 'post/edit.html', context)

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
