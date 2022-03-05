from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            )
        return self.create_user(username, password, **other_fields)

    def create_user(self, username,  password, **other_fields):

        if not username:
            raise ValueError(_('You must provide an email address'))

        user = self.model(username = username, **other_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractUser):

    username = models.CharField(max_length=10, unique=True)
    password = models.CharField('비밀번호', max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
