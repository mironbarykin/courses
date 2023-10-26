from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.random, name="random"),
    path("wiki/search/", views.search, name="search"),
    path("wiki/add/", views.add, name="add"),
    path("wiki/edit/<str:name>", views.edit, name="edit"),
    path("wiki/<str:name>", views.wiki, name="wiki"),
]
