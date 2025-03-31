from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password
from .models import *
from .forms import UserForm, PostForm, TagForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash



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


            return redirect('../login')

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
                form.save_m2m()
                return redirect('../myposts')
        else:
                form = PostForm()
                tag_form = TagForm()
                return render(request, 'createpost.html', {'form': form, 'tag_form': tag_form})

@login_required
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


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

@login_required
def userposts(request):
    posts = Post.objects.filter(author=request.user)  # Get user's posts
    return render(request, 'myposts.html', {'posts': posts})  # Render all posts

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Allow only the post author to edit
    if request.user != post.author:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('userposts')
    else:
        form = PostForm(instance=post)

    return render(request, 'editpost.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Allow only the post author to delete
    if request.user != post.author:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    post.delete()
    return redirect('userposts')
    # return JsonResponse({"message": "Post deleted successfully"}, status=204)

@login_required
def update_user(request):
    storage = messages.get_messages(request)
    storage.used = True
    user = request.user  # Get the logged-in user
    tags = user.tags.all()  # Fetch user's current tags

    if request.method == "POST":
        user_form = UserForm(request.POST)
        tag_form = TagForm(request.POST)

        if user_form.is_valid() or tag_form.is_valid():  # Ensure both forms are valid
            # Update username
            user.username = user_form.cleaned_data['Username']

            # Update password securely
            new_password = user_form.cleaned_data['Password']
            confirm_password = request.POST.get('Confirm_Password')
            if new_password==confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # ✅ Keep user logged in

            else:
                messages.error(request, "Passwords do not match!")  # ✅ Show error
                return render(request, 'account.html', {'form': user_form, 'tag_form': tag_form})

                # Update user's tags
            selected_tags = tag_form.cleaned_data['tags']
            user.tags.set(selected_tags)  #  Correct ManyToMany relationship update

            messages.success(request, "Account updated successfully!")  # ✅ Success message
            return redirect('userposts')

    else:
        # Prepopulate form with existing user data
        user_form = UserForm(initial={'Email': user.email, 'Username': user.username})
        tag_form = TagForm(initial={'tags': tags})

    return render(request, 'account.html', {'form': user_form, 'tag_form': tag_form})



@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    tracker, created = Liketrack.objects.get_or_create(user=request.user, postid=post)
    if not created:
        if tracker.likes:
            post.likes -= 1
            tracker.likes = False
        else:
            if tracker.dislikes:
                post.dislikes -= 1
                tracker.dislikes = False
            post.likes += 1
            tracker.likes = True
        tracker.save()
    else:
        # First-time like
        post.likes += 1
        tracker.likes = True
        tracker.save()

    post.save()
    post.author.update_likes_dislikes()
    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})

@login_required
def post_dislike(request, post_id):
    # post = get_object_or_404(Post, id=post_id)
    # post.dislikes+=1
    # post.save()
    # post.author.update_likes_dislikes()
    # return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})
    post = get_object_or_404(Post, id=post_id)
    tracker, created = Liketrack.objects.get_or_create(user=request.user, postid=post)
    if not created:
        if tracker.dislikes:
            post.dislikes -= 1
            tracker.dislikes = False
        else:
            if tracker.likes:
                post.likes -= 1
                tracker.likes = False
            post.dislikes += 1
            tracker.dislikes = True
        tracker.save()
    else:
        # First-time like
        post.dislikes += 1
        tracker.dislikes = True
        tracker.save()

    post.save()
    post.author.update_likes_dislikes()
    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})


@login_required
def comment_like(request, comment_id):
    post = get_object_or_404(Comment, id=comment_id)
    tracker, created = Liketrack.objects.get_or_create(user=request.user, commentid=post)
    if not created:
        if tracker.likes:
            post.likes -= 1
            tracker.likes = False
        else:
            if tracker.dislikes:
                post.dislikes -= 1
                tracker.dislikes = False
            post.likes += 1
            tracker.likes = True
        tracker.save()
    else:
        # First-time like
        post.likes += 1
        tracker.likes = True
        tracker.save()

    post.save()
    post.author.update_likes_dislikes()
    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})
    # post.likes+=1
    # post.save()
    # post.author.update_likes_dislikes()
    # return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})

@login_required
def comment_dislike(request, comment_id):
    post = get_object_or_404(Comment, id=comment_id)
    tracker, created = Liketrack.objects.get_or_create(user=request.user, commentid=post)
    if not created:
        if tracker.dislikes:
            post.dislikes -= 1
            tracker.dislikes = False
        else:
            if tracker.likes:
                post.likes -= 1
                tracker.likes = False
            post.dislikes += 1
            tracker.dislikes = True
        tracker.save()
    else:
        # First-time like
        post.dislikes += 1
        tracker.dislikes = True
        tracker.save()

    post.save()
    post.author.update_likes_dislikes()
    return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})

def aboutus(request):
    return render(request, 'aboutus.html')

    # post.dislikes+=1
    # post.save()
    # post.author.update_likes_dislikes()
    # return JsonResponse({'likes': post.likes, 'dislikes': post.dislikes})


