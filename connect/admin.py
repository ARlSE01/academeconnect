from django.contrib import admin
from .models import *
from chatapp.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tags)
admin.site.register(Liketrack)