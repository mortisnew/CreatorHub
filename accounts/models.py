from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError

from .manager import UserManager

class Gender(models.TextChoices):
    MALE = 'M'
    FEMALE = 'F'

class CreatorUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(unique=True, max_length=200)
    age = models.PositiveSmallIntegerField()
    bio = models.TextField(blank=True)
    gender = models.CharField(choices=Gender.choices,max_length=1,blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','age']

    def __str__(self):
        return f'{self.username} - {self.email}'

class CreatorLink(models.Model):
    creator = models.ForeignKey(CreatorUser, on_delete=models.CASCADE,
                                related_name='links')
    title = models.CharField(max_length=50)
    link = models.URLField()


class Blocklist(models.Model):
    blocker = models.ForeignKey(CreatorUser, on_delete=models.CASCADE,
                             related_name='blocker')
    blocked = models.ForeignKey(CreatorUser, on_delete=models.CASCADE,
                               related_name='blocked')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['blocker', 'blocked'],
                name='unique_blacklist'
            )
        ]