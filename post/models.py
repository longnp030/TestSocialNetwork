from django.db import models

from user.models import *

# Create your models here.

def image_upload_location(instance, filename):
    return 'post/images/p%s-%s.%s' % (instance.id, instance.author.username, filename.split('.')[1])


class PostImage(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_column='id')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column='owner')
    image = models.ImageField(max_length=255, upload_to=image_upload_location, db_column='image', null=True)
    
    class Meta:
        db_table = 'postimage'
        managed = False


class Post(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_column='id')
    author = models.ForeignKey(
        User,
        related_name='creator', verbose_name='author',
        on_delete=models.CASCADE,
        db_column='author'
    )
    receiver = models.ForeignKey(
        User,
        related_name='post_receiver', verbose_name='post_receiver',
        on_delete=models.CASCADE,
        db_column='receiver',
        null=True, blank=True
    )
    text = models.CharField(max_length=1000, blank=True, null=True, db_column='text')
    images = models.ManyToManyField(
        to=PostImage,
        verbose_name='images',
        db_column='images'
    )
    created = models.DateTimeField(auto_now_add=True, db_column='created')
    modified = models.DateTimeField(auto_now=True, db_column='modified')

    def __str__(self):
        return self.author.username + '-' + self.text

    class Meta:
        db_table = 'post'
        managed = False


class Reaction(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_column='id')
    post = models.ForeignKey(
        Post,
        related_name='reaction', verbose_name="post's reactions",
        db_column='post',
        on_delete=models.CASCADE,
    )
    like = models.IntegerField(
        verbose_name='like', blank=True, null=True,
        db_column='like'
    )
    '''love = models.IntegerField(
        verbose_name='love', blank=True, null=True,
        db_column='love'
    )
    care = models.IntegerField(
        verbose_name='care', blank=True, null=True,
        db_column='care'
    )
    haha = models.IntegerField(
        verbose_name='haha', blank=True, null=True,
        db_column='haha'
    )
    sad = models.IntegerField(
        verbose_name='sad', blank=True, null=True,
        db_column='sad'
    )
    angry = models.IntegerField(
        verbose_name='angry', blank=True, null=True,
        db_column='angry'
    )'''
    class Meta:
        db_table = 'reaction'
        managed = False


class Comment(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_column='id')
    commentor = models.ForeignKey(
        User,
        verbose_name='commentor',
        on_delete=models.CASCADE,
        db_column='commentor'
    )
    post = models.ForeignKey(
        Post,
        verbose_name='post commented on',
        on_delete=models.CASCADE,
        db_column='post',
    )
    content = models.CharField(
        verbose_name='comment',
        max_length=1000,
        blank=True, null=True,
        db_column='content',
    )
    written = models.DateTimeField(auto_now_add=True, db_column='written')
    modified = models.DateTimeField(auto_now=True, db_column='modified')

    def __str__(self):
        return self.commentor + '-' + self.content

    class Meta:
        db_table = 'comment'
        managed = False
