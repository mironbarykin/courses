from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("create", views.create_view, name="create"),
    path("episode/<int:id>", views.episode_view, name="episode"),
    path("podcast/<int:id>", views.podcast_view, name="podcast"),
    path("queue", views.queue_view, name="queue"),
    path("subscriptions", views.subscriptions_view, name="subscriptions")
]
