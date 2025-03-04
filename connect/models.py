from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)  # Unique username
    email = models.EmailField(unique=True, blank=False, null=False)  # Required and unique email
    password = models.CharField(max_length=255, blank=False, null=False)  # Ensuring non-null password
    likes = models.PositiveIntegerField(default=0)  # Positive number for likes
    dislikes = models.PositiveIntegerField(default=0)  # Positive number for dislikes
    blocked = models.ManyToManyField("self",symmetrical=False, blank=True, related_name="blocked_by")  
    tags = models.CharField(max_length=255, blank=False, null=False, default="HTML") 
    # ManyToManyField allows users to block multiple users

    class Meta:
        db_table='User'


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=True,null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='Posts'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table='Comments'

