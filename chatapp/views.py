from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect("../login")
    chat_group=get_object_or_404(ChatGroup)
    chat_messages=chat_group.chat_messages.all()
    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context={
                'message':message,
                'user':request.user,

            }
            return render(request,'chatapp/partials/chat_message_p.html',context)
    return render(request, 'chat.html',{'chat_messages':chat_messages,'form' : form})
