import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    return render(request, "network/index.html")

def profile(request, id):
    return render(request, "network/profile.html", { "userdisplayed_user": User.objects.get(pk=id) })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# API Functions

@csrf_exempt
@login_required
def posting(request):
    if request.method != "POST":
        return JsonResponse({"messsage": "POST request required."}, status=400)

    data = json.loads(request.body)
    
    # Check for login.
    try:
        author = User.objects.get(username=request.user)
    except:
        return JsonResponse({"message": "Please log in!"}, status=400)

    # Check for content is added.
    content = data.get("content", "")
    if content == "":
        return JsonResponse({"message": "Please input content!"}, status=400)
        
    # Creating post.
    post = Post(
        author=author,
        content=content
    )
    post.save()
    return JsonResponse({"message": "Posted successfully."}, status=201)


def posts(request, type):
    if type == 'allposts':
        posts = Post.objects.all()
        posts = posts.order_by("-timestamp").all()
        pagin = Paginator(posts, 10)

        return JsonResponse([[{**post.serialize(), **{"userid": request.user.id}} for post in pagin.page(i)] for i in pagin.page_range], safe=False)
    if type == 'follow':
        posts = Post.objects.filter(author__in=request.user.followings.all())
        posts = posts.order_by("-timestamp").all()
        pagin = Paginator(posts, 10)
        
        return JsonResponse([[{**post.serialize(), **{"userid": request.user.id}} for post in pagin.page(i)] for i in pagin.page_range], safe=False)
    else:
        try:
            posts = Post.objects.filter(author = User.objects.get(pk=int(type)))
            posts = posts.order_by("-timestamp").all()
            pagin = Paginator(posts, 10)

            return JsonResponse([[{**post.serialize(), **{"userid": request.user.id}} for post in pagin.page(i)] for i in pagin.page_range], safe=False)
        except:
            pass

@csrf_exempt
@login_required
def post(request, post_id):
    post = Post.objects.get(id=post_id)
    userid = request.user.id
    if userid < 1:
        userid = 0
    if request.method == "PUT":
        data = json.loads(request.body)
        # Check for content is added.
        action = data.get("type", "")
        if action == 'liking':
            liked = data.get("liked", "")
            if liked == True:
                post.likedby.add(request.user)
            elif liked == False:
                post.likedby.remove(request.user)
            else:
                return JsonResponse({"message": "Something went wrong."}, status=400)
            # Creating post.
            post.save()
            return JsonResponse({"message": "Posted successfully.", "count": post.likedby.count()}, status=201)
        elif action == 'editing':
            content = data.get("content", "")
            post.content = content
            post.save()
            return JsonResponse({"message": "Posted successfully.", "content": post.content}, status=201)
    elif request.method == "GET":
        return JsonResponse({**post.serialize(), **{"userid": userid}}, safe=False)
    else:
        return JsonResponse({"messsage": "PUT request required."}, status=400)


@csrf_exempt
@login_required
def user(request, action):
    data = json.loads(request.body)
    if action == 'follow':
        profile = data.get("profile", "")
        User.objects.get(pk=int(profile)).followers.add(request.user)
        return JsonResponse({"message": "Followed successfully!"}, safe=False)
    elif action == 'unfollow':
        profile = data.get("profile", "")
        User.objects.get(pk=int(profile)).followers.remove(request.user)
        return JsonResponse({"message": "Unfollowed successfully!"}, safe=False)
    else:
        return JsonResponse({"message": "Something went wrong!"}, safe=False)

