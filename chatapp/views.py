from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse,JsonResponse,Http404
from django.contrib.auth.hashers import make_password
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def home(request,chatroom_name="public_group"):
    chat_group=get_object_or_404(ChatGroup,group_name=chatroom_name)
    chat_messages=chat_group.chat_messages.all()
    other_user=None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            return Http404( )
        for member in chat_group.members.all():
            if member != request.user:
                other_user=member
                break
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
    else:
        form = ChatmessageCreateForm()
    context={'chat_messages':chat_messages,'form' : form,'other_user':other_user,'chatroom_name':chatroom_name}
    return render(request, 'chat.html',context)



@login_required
def display_all_users(request):
    users = User.objects.all()
    return render(request, 'displayallusers.html', {'users':users})

def get_or_create_chatroom(request,username):
    other_user = User.objects.get(username=username)
    my_private_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_private_chatrooms.exists():
        for chatroom in my_private_chatrooms:
            if other_user in chatroom.members.all():
                return redirect('chatroom', chatroom.group_name)

    chatroom = ChatGroup.objects.create(is_private=True)
    chatroom.members.add(other_user, request.user)
    return redirect('chatroom', chatroom.group_name,{'other_user':other_user})


def selecttags(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.cleaned_data['tags']  # Use correct key
            users = User.objects.filter(tags=tag)
            return render(request, 'displayallusers.html', {'users': users})
    else:
        form = TagForm()
    return render(request, 'selecttags.html', {'form': form})

def user_chatgroups(request):
    # Fetch groups where the user is a member
    chatgroups = ChatGroup.objects.filter(members=request.user)
    print(chatgroups)
    return render(request, 'user_chatgroups.html', {'chatgroups': chatgroups})
