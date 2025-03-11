from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("../login")
    return render(request, 'chat.html')
