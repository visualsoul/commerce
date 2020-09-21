from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, WatchList
from .forms import CreateListing


def index(request):
    active_listings = AuctionListing.objects.all()
    watch_list = WatchList.objects.filter(user=request.user.id)
    context = {
        "active_listings": active_listings,
        "watchlist": watch_list
    }
    return render(request, "auctions/index.html", context)

def listing(request, pk):
    listing = AuctionListing.objects.get(id=pk)
    context = {
        "listing": listing
    }
    return render(request, "auctions/listing.html", context)

@login_required(login_url='login')
def watchlist(request):
    watch_list = WatchList.objects.filter(user=request.user.id)

    context = {
        'watchlist': watch_list
    }
    return render(request, "auctions/watchlist.html", context)


@login_required(login_url='login')
def create_listing(request):
    if request.POST:
        form = CreateListing(request.POST)
        if form.is_valid():
            db_data = form.save()
            db_data.user = request.user
            db_data.save()
            return HttpResponseRedirect(reverse('index'))
    form = CreateListing()
    context = {'form': form}
    return render(request, 'auctions/create_listing.html', context)

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
