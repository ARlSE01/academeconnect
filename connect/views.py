from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
# from models import *

def homepage(request):
    return render(request, 'homepage.html')


# Create your views here.
