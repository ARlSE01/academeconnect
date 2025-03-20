from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("home", views.home, name="home"),
    path("users", views.display_all_users, name="display_all_users"),
    path("selecttags", views.selecttags, name="selecttags"),
    path("privatechat/<str:username>", views.get_or_create_chatroom, name="start-chat"),
    path("room/<chatroom_name>", views.home, name="chatroom"),

    # login-section
]