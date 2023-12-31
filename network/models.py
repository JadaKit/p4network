from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    
    
class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    date = models.DateTimeField(null=True)
    content = models.TextField(default='')
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
