import string

from django.contrib.auth.models import AbstractUser
from django.db import models
import random


# Create your models here.
def generate_random_username():
    return "User" + ''.join(random.choices(string.digits, k=4))

def user_profile_picture_path():
    # Store profile pictures in 'profile_pics/user_<id>/<filename>'
    var=random.randint(0,9)
    return f'static/uploads/propic_{var}.jpg'

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)  # Unique username
    email = models.EmailField(unique=True, blank=False, null=False)  # Required and unique email
    password = models.CharField(max_length=255, blank=False, null=False)  # Ensuring non-null password
    likes = models.PositiveIntegerField(default=0)  # Positive number for likes
    dislikes = models.PositiveIntegerField(default=0)  # Positive number for dislikes
    blocked = models.ManyToManyField("self",symmetrical=False, blank=True, related_name="blocked_by")
    random_username = models.CharField(max_length=150, blank=False, null=False, default=generate_random_username)

    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True,default=user_profile_picture_path)


    def update_likes_dislikes(self):
        """Update the user's total likes and dislikes based on their posts/comments."""
        postlikes = self.posts.aggregate(models.Sum('likes'))['likes__sum'] or 0
        commentlikes = self.comments.aggregate(models.Sum('likes'))['likes__sum'] or 0
        commentdislikes = self.comments.aggregate(models.Sum('dislikes'))['dislikes__sum'] or 0
        postdislikes = self.posts.aggregate(models.Sum('dislikes'))['dislikes__sum'] or 0
        self.likes = postlikes+commentlikes
        self.dislikes = postdislikes+commentdislikes
        self.save()


    class Meta:
        db_table='User'


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=True,null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    class Meta:
        db_table='Posts'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def depth(self):
        depth = 0
        parent = self.parent
        while parent:
            depth += 1
            parent = parent.parent
        return depth

    class Meta:
        db_table='Comments'


class Tags(models.Model):
    TAG_CHOICES = [
        ('HTML', 'HTML'),
        ('CSS', 'CSS'),
        ('JS', 'JavaScript'),
        ('Python', 'Python'),
        ('Django', 'Django'),
    ]
    name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(User, related_name='tags', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tags"  # Explicit table name (optional)

class Liketrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liketracksuser")
    postid = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liketrackpostid",null=True)
    commentid = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="liketrackcommentid",null=True)
    likes = models.BooleanField(default=False)
    dislikes = models.BooleanField(default=False)

    class Meta:
        db_table = "liketrack"
