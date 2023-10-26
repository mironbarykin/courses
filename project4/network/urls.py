
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile, name="profile"),
    # API Functions
    path("post", views.posting, name="posting"),
    path("posts/<str:type>", views.posts, name="posts"),
    path("profile/posts/<int:type>", views.posts, name="posts"),
    path("post/<int:post_id>", views.post, name="post"),
    path("user/<str:action>", views.user, name="user")
]
