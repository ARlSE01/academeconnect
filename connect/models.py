from django.db import models

class Comments(models.Model):
    comment = models
# Create your models here.
class User(models.Model):
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