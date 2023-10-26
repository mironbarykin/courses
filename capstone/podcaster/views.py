from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from podcaster.models import User, Episode, Podcast

from .services.search import process
from .services.posting import posting_episode, posting_podcast, posting_comment
from .services.actions import action


def index(request):
    if request.method == 'POST':
        viewname, kwargs = process(question=request.POST.get("q"))
        if viewname == 'index':
            return render(request, 'podcaster/index.html', kwargs)
        return HttpResponseRedirect(reverse(viewname=viewname, kwargs=kwargs))
    else:
        return render(request, 'podcaster/index.html',
                      {'podcasts': Podcast.objects.all(), 'episodes': Episode.objects.all()})


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'podcaster/login.html', {'message': 'Invalid username and/or password.'})
    else:
        return render(request, 'podcaster/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        age = request.POST['age']
        country = request.POST['country']
        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'podcaster/register.html', {'message': 'Passwords must match.'})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'podcaster/register.html', {'message': 'Username already taken.'})
        
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'podcaster/register.html')


def create_view(request):
    if request.method == 'POST':
        if request.POST['action'] == 'episode':
            posting_episode(request)
            return HttpResponseRedirect(reverse('index'))
        elif request.POST['action'] == 'podcast':
            posting_podcast(request)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('create'))
    else:
        return render(request, 'podcaster/create.html', {
            'is_author': request.user.is_author()
        })


def episode_view(request, id):
    if request.method == 'POST':
        # Looking for special action
        if request.POST['action'] == 'comment':
            posting_comment(request, id)
        else:
            action(request.user, id, request.POST['action'])
        return HttpResponseRedirect(reverse('episode', kwargs={'id': id}))
    else:
        return render(request, 'podcaster/_episode.html', {
            'episode': Episode.objects.get(id=id),
            'requester': request.user
        })


def podcast_view(request, id):
    if request.method == 'POST':
        action(request.user, id, request.POST['action'])
        return HttpResponseRedirect(reverse('podcast', kwargs={'id': id}))
    else:
        return render(request, 'podcaster/_podcast.html', {
            'podcast': Podcast.objects.get(id=id),
            'requester': request.user
        })


def queue_view(request):
    return render(request, 'podcaster/_queue.html', {
        'episodes': Episode.objects.filter(queuned_users__username__icontains=request.user.username)
    })


def subscriptions_view(request):
    return render(request, 'podcaster/_subscriptions.html', {
        'podcasts': Podcast.objects.filter(subscribers__username__icontains=request.user.username)
    })
