from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password
from .models import *
from .forms import UserForm, PostForm


# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')


# def registration_old(request):
#     return render(request, 'registration_old.html')


# def reg(request):
#     if request.method == "POST":
#         username = request.POST.get("name")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         tags = request.POST.getlist("tags")  # Get list of selected checkboxes
#
#         # Ensure at least one tag is selected
#         if not tags:
#             messages.error(request, "Please select at least one tag.")
#             return redirect("../registration")
#
#         # Convert list of tags into a comma-separated string (e.g., "HTML,CSS,JavaScript")
#         tags_str = ",".join(tags)
#
#         # Check if email already exists
#         if User.objects.filter(email=email).exists():
#             return HttpResponse("Email already registered!")
#             # return redirect("../registration")
#
#         # Create user and hash password
#         u = User(username=username, email=email, password=make_password(password), tags=tags_str)
#         u.save()
#
#         return HttpResponse("Registration successful!")
#         # messages.success(request, "Registration successful!")
#         # return redirect("login")  # Redirect to login page after registration
#
#     return render(request, "registration_old.html")

def registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Username']
            email = form.cleaned_data['Email']
            password = form.cleaned_data['Password']
            tags = ', '.join(form.cleaned_data['Tags'])  # Convert selected tags to a string

            # Hash the password for security
            hashed_password = make_password(password)

            # Create and save the user
            user = User(username=username, email=email, password=hashed_password, tags=tags)
            user.save()

            return HttpResponse('DONE GOOD JOB')

    else:
        form = UserForm()

    return render(request, 'registration.html', {'form': form})

def createpost(request):
        form = PostForm()
        return render(request, 'createpost.html', {'form': form})


