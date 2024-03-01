import uuid
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    """个人账号信息"""
    id = models.UUIDField(primary_key=True, editable=False,
                          unique=True, default=uuid.uuid4)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, 
                                      default='profiles/user-default.png', upload_to='profiles/')
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_youtube = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ['created']
    

class Skill(models.Model):
    """开发者的技能（多对一关系）"""
    id = models.UUIDField(primary_key=True, editable=False,
                          unique=True, default=uuid.uuid4)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return str(self.name)


class Message(models.Model):
    """用户之间发送消息"""
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read= models.BooleanField(default=False, null=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)

    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['is_read', '-created']



