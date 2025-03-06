from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password
from .models import *
from .forms import UserForm, PostForm, TagForm, CommentForm
from django.contrib.auth.decorators import login_required



# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        tagform = TagForm(request.POST)
        if form.is_valid() and tagform.is_valid():
            username = form.cleaned_data['Username']
            email = form.cleaned_data['Email']
            password = form.cleaned_data['Password']
            tags = tagform.cleaned_data['tags']
            # tags = ', '.join(form.cleaned_data['Tags'])  # Convert selected tags to a string

            # Hash the password for security
            hashed_password = make_password(password)

            # Create and save the user
            user = User(username=username, email=email, password=hashed_password)
            # user = User(username=username, email=email, password=hashed_password, tags=tags)
            user.save()
            user.tags.set(tags)


            return HttpResponse('DONE GOOD JOB')

    else:
        form = UserForm()
        TAGS = TagForm()

    return render(request, 'registration.html', {'form': form , 'tags': TAGS})

@login_required
def createpost(request):
        if request.method=='POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('../createpost')
        else:
                form = PostForm()
                return render(request, 'createpost.html', {'form': form})

def viewposts(request):
    posts= Post.objects.all()
    return render(request, 'viewpost.html', {'posts': posts})

@login_required
def add_comment(request, post_id):
    post= get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            parent_id=request.POST.get('parent_id')
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                comment.parent = parent_comment

            comment.save()
            return redirect("post_detail", post_id=post.id)
    return redirect("post_detail", post_id=post.id)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes+=1
    post.save()
    post.author.update_likes_dislikes()
    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})

@login_required
def post_dislike(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.dislikes+=1
    post.save()
    post.author.update_likes_dislikes()
    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})

@login_required
def comment_like(request, comment_id):
    post = get_object_or_404(Comment, id=comment_id)
    post.likes+=1
    post.save()
    post.author.update_likes_dislikes()
    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})

@login_required
def comment_dislike(request, comment_id):
    post = get_object_or_404(Comment, id=comment_id)
    post.dislikes+=1
    post.save()
    post.author.update_likes_dislikes()
    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})


