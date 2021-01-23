import collections
from django import db
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.

def avatar_upload_location(instance, filename):
    return 'user/images/u%s.%s' % (instance.id, filename.split('.')[1])


class UserManager(BaseUserManager):  # MyUserManager
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):  # MyUser
    id = models.AutoField(primary_key=True, unique=True, db_column='id')
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='user name',
        max_length=20,
        unique=True,
        db_column='username'
    )
    avatar = models.ImageField(max_length=255, upload_to=avatar_upload_location, db_column='avatar', null=True)
    is_active = models.BooleanField(default=True, db_column='is_active')
    is_admin = models.BooleanField(default=False, db_column='is_admin')
    is_staff = models.BooleanField(default=False, db_column='is_staff')
    last_login = models.DateTimeField(blank=True, null=True, db_column='last_login')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    class Meta:
        db_table = 'user'
        managed = False


class Friendship(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_column='id')
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user1',
        db_column='user1',
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user2',
        db_column='user2',
    )
    added = models.DateTimeField(auto_now_add=True, db_column='added')

    class Meta:
        db_table = 'friendship'
        managed = False

    def __str__(self):
        return self.user1.username + '-' + self.user2.username


class FriendRequest(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_column='id')
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sender',
        db_column='sender',
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver',
        db_column='receiver',
    )
    sended = models.DateTimeField(auto_now_add=True, db_column='sended')
    STATUS = (
        ('IDLE', 0),
        ('ACCEPTED', 1),
        ('REJECTED', 2),
    )
    status = models.IntegerField(verbose_name='status', choices=STATUS, default='IDLE', db_column='status')

    class Meta:
        db_table = 'friendrequest'
        managed = False

    def __str__(self):
        return self.sender.username + '-' + self.receiver.username

class Block(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_column='id')
    blocker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocker',
        db_column='blocker',
    )
    blockee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blockee',
        db_column='blockee',
    )
    blocked = models.DateTimeField(auto_now_add=True, db_column='blocked')

    class Meta:
        db_table = 'block'
        managed = False

    def __str__(self):
        return self.blocker.username + '-' + self.blockee.username
