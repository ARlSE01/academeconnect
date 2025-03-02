from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password
from connect.models import *
# from models import *

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')


def registration(request):
    return render(request, 'registration.html')


# def reg(request):
#     if request.method == "POST":
#         username = request.POST.get("name")
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         # Check if email already exists
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already registered!")
#             return redirect("register")

#         # Create user and hash password
#         u = User(username=username, email=email, password=make_password(password))
#         u.save()

#         messages.success(request, "Registration successful!")
#         return redirect("login")  # Redirect to login page after registration

#     return render(request, "register.html")


def reg(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        tags = request.POST.getlist("tags")  # Get list of selected checkboxes

        # Ensure at least one tag is selected
        if not tags:
            messages.error(request, "Please select at least one tag.")
            return redirect("../registration")

        # Convert list of tags into a comma-separated string (e.g., "HTML,CSS,JavaScript")
        tags_str = ",".join(tags)

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered!")
            # return redirect("../registration")

        # Create user and hash password
        u = User(username=username, email=email, password=make_password(password), tags=tags_str)
        u.save()

        return HttpResponse("Registration successful!")
        # messages.success(request, "Registration successful!")
        # return redirect("login")  # Redirect to login page after registration

    return render(request, "registration.html")

