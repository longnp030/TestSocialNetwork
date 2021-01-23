from django.db import models
import uuid

from user.models import *

# Create your models here.

class Message(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_column='id')
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_sender',
        verbose_name='chat_sender',
        db_column='sender',
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_receiver',
        verbose_name='chat_receiver',
        db_column='receiver',
    )
    content = models.TextField(verbose_name='content', db_column='content')
    chatbox = models.ForeignKey(
        'ChatBox',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='chatbox',
        db_column='chatbox',
    )
    sent = models.DateTimeField(auto_now_add=True, db_column='sent')

    def __str__(self):
        return '(' + self.sender.username + '-' + self.receiver.username + ') ' + self.content
    
    class Meta:
        db_table = 'message'
        managed = False


class ChatBox(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_column='id', default=1)
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_user1',
        verbose_name='chat_user1',
        db_column='user1',
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_user2',
        verbose_name='chat_user2',
        db_column='user2',
    )
    created = models.DateTimeField(auto_now_add=True, db_column='created')
    name = models.CharField(
        max_length=45,
        verbose_name='name',
        db_column='name')

    def save(self, *args, **kwargs):
        #self.name = self.user1.username + '-' + self.user2.username
        if not self.name:
            self.name = str(self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chatbox'
        managed = False
