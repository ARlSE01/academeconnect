from django.contrib import admin
from .models import *
from connect.models import *


# Register your models here.
admin.site.register(ChatGroup)
admin.site.register(GroupMessage)