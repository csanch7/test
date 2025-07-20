
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:user>", views.userposts, name="userposts"),
    path("<str:user>/following", views.followingposts, name="followingposts"),
    path("edit/<int:postId>", views.edit, name = "edit"),
    

    # API Routes
    path("posts", views.compose, name="compose"),
    path("posts/allposts", views.allposts, name="allposts"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("follow/<str:user>", views.follow, name="follow"),

    
    
]
