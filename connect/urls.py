from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('registration',views.registration),
    path('createpost',views.createpost, name="createpost"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('viewposts', views.viewposts, name='viewposts'),
    path('post/viewposts', views.viewposts, name='viewposts'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('like/post/<int:post_id>/', views.post_like, name='like_post'),
    path('dislike/post/<int:post_id>/', views.post_dislike, name='dislike_post'),
    path('like/comment/<int:comment_id>/', views.comment_like, name='like_comment'),
    path('dislike/comment/<int:comment_id>/', views.comment_dislike, name='dislike_comment'),
    path('myposts/', views.userposts, name='userposts'),  # Show all posts
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),  # Edit a Post
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),  # Delete a Post
    path('account',views.update_user, name='update_user'),
]