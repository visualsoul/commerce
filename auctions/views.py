from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import User, AuctionListing, WatchList
from .forms import CreateListing


def index(request):
    active_listings = AuctionListing.objects.all()
    watch_list_counter = WatchList.objects.filter(user=request.user.id).count()
    context = {
        "active_listings": active_listings,
        "watchlist_counter": watch_list_counter
    }
    return render(request, "auctions/index.html", context)

def listing(request, pk):
    watch_list_counter = WatchList.objects.filter(user=request.user.id).count()
    listing = AuctionListing.objects.get(id=pk)
    is_watching = False

    #TODO: Needs reworking
    if request.POST.get('create_watchlist_btn'):
        # Check if object exists, if not catch exception and add object
        try:
            is_watching = WatchList.objects.get(user=request.user, listing=listing).is_watching
        except ObjectDoesNotExist as e:
            WatchList.objects.create(user=request.user, listing=listing, is_watching=True).save()
            is_watching = True
        return HttpResponseRedirect(reverse("watchlist"))

    elif request.POST.get('delete_watchlist_btn'):
        WatchList.objects.get(user=request.user, listing=listing).delete()
        return HttpResponseRedirect(reverse("watchlist"))

    context = {
        "listing": listing,
        "watchlist_counter": watch_list_counter,
        "is_watching": is_watching
    }
    return render(request, "auctions/listing.html", context)

@login_required(login_url='login')
def watchlist(request):
    watch_list_counter = WatchList.objects.filter(user=request.user.id).count()
    watch_list = WatchList.objects.filter(user=request.user.id)

    if request.POST:
        listing_id = request.POST.get('listing_id')
        listing = AuctionListing.objects.get(pk=listing_id)
        WatchList.objects.filter(user=request.user, listing=listing).delete()
        return HttpResponseRedirect(reverse("watchlist"))
    context = {
        'watchlist': watch_list,
        'watchlist_counter': watch_list_counter
    }
    return render(request, "auctions/watchlist.html", context)


@login_required(login_url='login')
def create_listing(request):
    watch_list_counter = WatchList.objects.filter(user=request.user.id).count()
    if request.POST:
        form = CreateListing(request.POST)
        if form.is_valid():
            db_data = form.save()
            db_data.user = request.user
            db_data.save()
            return HttpResponseRedirect(reverse('index'))
    form = CreateListing()
    context = {'form': form,
               'watchlist_counter': watch_list_counter}
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
