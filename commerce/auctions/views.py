from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Bid


def index(request):
    listings = Listing.objects.filter(status="active")
    return render(request, "auctions/index.html", {
        'listings': listings
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def listing(request, id):
    listing = Listing.objects.get(id=id)
    lastbid = listing.bids.last()
    if request.method == "POST":
        author = request.user
        if request.POST["action"] == "comment":
            content = request.POST["content"]
            

            comment = Comment(author=author, content=content, listing=listing)
            comment.save()

            return HttpResponseRedirect(reverse("listing", args=[id]))
        if request.POST["action"] == "bid":
            amount = request.POST["amount"]
            if amount == None:
                amount = 0
            else:
                amount = int(amount)
            
            if amount < (lastbid.amount or listing.starting_bid):
                return render(request, "auctions/error.html", {
                'details': "Your bid is lower when minimal or last bid."
                })

            
            bid = Bid(author=author, amount=amount, listing=listing)
            bid.save()

            return HttpResponseRedirect(reverse("listing", args=[id]))
        if request.POST["action"] == "watchlist_add":
            request.user.watchlist.add(listing)

            return HttpResponseRedirect(reverse("listing", args=[id]))
        if request.POST["action"] == "watchlist_remove":
            request.user.watchlist.remove(listing)

            return HttpResponseRedirect(reverse("listing", args=[id]))
        if request.POST["action"] == "close":
            listing.status = "closed"
            listing.save()

            return HttpResponseRedirect(reverse("listing", args=[id]))
    else:
        if listing in request.user.watchlist.all():
            is_in_watchlist = True
        else:
            is_in_watchlist = False
        return render(request, "auctions/listing.html", {
            'visitor': request.user,
            'watchlist': is_in_watchlist,
            'listing': listing,
            'bid': lastbid,
            'comments': listing.comments.all(),
        })


@login_required
def create_listing(request):
    if request.method == "POST":

        author = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.POST["image"]
        category = request.POST["category"]

        listing = Listing(author=author, title=title, description=description, starting_bid=starting_bid, image=image, category=category, status="active")
        listing.save()

        bid = Bid(author=author, amount=starting_bid, listing=listing)
        bid.save()

        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    else:
        return render(request, "auctions/create_listing.html")


def categories(request):
    if request.method == "POST":
        category = request.POST["category"]
        listings = Listing.objects.filter(category=category)
        return render(request, "auctions/categories.html", {
            'listings': listings
        })

    else:
        return render(request, "auctions/categories.html", {
            'listings': None
        })


@login_required
def watchlist(request):
    elements = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        'elements': elements
    })