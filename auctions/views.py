from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import User, AuctionListing, WatchList, Bid, Comment
from .forms import CreateListing, PlaceBid, CommentForm

categories = {1: "Laptop", 2: "Desktop PC", 3: "CPU", 4: "Memory (RAM)", 5: "Motherboards", 6: "Graphics Cards",
                  7: "Networking", 8: "Audio", 9: "Other Components"}

def index(request):
    active_listings = AuctionListing.objects.filter(active=True)
    watch_list_counter = WatchList.objects.filter(user=request.user.id).count()
    context = {
        "active_listings": active_listings,
        "watchlist_counter": watch_list_counter
    }
    return render(request, "auctions/index.html", context)

def listing(request, pk):
    watch_list_counter = WatchList.objects.filter(user=request.user.id).count()
    _listing = AuctionListing.objects.get(id=pk)
    watching = WatchList.objects.filter(user=request.user.id, listing=_listing).count()
    comment_form = CommentForm()
    place_bid_form = PlaceBid()
    bids = _listing.bidItem.all()
    comments = _listing.comment_set.all()

    if len(comments) > 0:
        comments = comments.order_by('-dt')

    max_bid = 0
    current_bidder = None
    message = None

    if len(bids) > 0:
        max_bid = bids.order_by('-amount')[0].amount
        current_bidder = bids.order_by('-amount')[0].bidder

    # --------------------------- Comments form -------------------------------------------------
    if request.POST.get('submit_comment'):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_message = request.POST.get('message')
            print(comment_message)
            comment_instance = Comment(user=request.user, listing=_listing, message=comment_message)
            comment_instance.save()
        return HttpResponseRedirect(reverse('listing', args=[_listing.id]))

    # -------------------------------------------------------------------------------------------

    # --------------------------- place bid form ------------------------------------------------

    if request.POST.get('place_bid'):
        place_bid_form = PlaceBid(request.POST)
        amount = request.POST.get('amount')
        user = request.user
        bids = _listing.bidItem.all()
        max_bid = 0
        if len(bids) > 0:
            max_bid = bids.order_by('-amount')[0].amount
        if float(amount) >= float(_listing.starting_bid):
            if float(amount) > float(max_bid):
                bid = Bid(bidder=user, listing=_listing, amount=float(amount))
                bid.save()
                print("Bid placed")
            else:
                message = 'Your bid needs to be higher than the current price'
                print(message)
        else:
            message = 'Your bid needs to be higher than the starting bid.'
            print(message)
        return HttpResponseRedirect(reverse("listing", args=[_listing.id]))
    #--------------------------------------------------------------------------------------------


    # ------------------------ watchlist button -------------------------------------------------
    if request.POST.get('create_watchlist_btn'):
        # Check if object exists, if not catch exception and add object
        try:
            is_watching = WatchList.objects.get(user=request.user, listing=_listing).is_watching
        except ObjectDoesNotExist:
            WatchList.objects.create(user=request.user, listing=_listing, is_watching=True).save()
        return HttpResponseRedirect(reverse("listing", args=[_listing.id]))

    if request.POST.get('delete_watchlist_btn'):
        WatchList.objects.get(user=request.user, listing=_listing).delete()
        return HttpResponseRedirect(reverse("listing", args=[_listing.id]))
    # --------------------------------------------------------------------------------------------

    # --------------------------- Close Auction Listing ------------------------------------------
    #TODO needs finishing need changes in teplate if active show this or else show different template structure..
    if request.POST.get('close_auction'):
        listItem = AuctionListing.objects.get(pk=_listing.id)
        listItem.active = False
        listItem.save()
        print('List Item closed.')
        return HttpResponseRedirect(reverse("listing", args=[_listing.id]))

    # --------------------------------------------------------------------------------------------

    context = {
        "listing": _listing,
        "watchlist_counter": watch_list_counter,
        'watching': watching,
        'place_bid_form': place_bid_form,
        'current_price': max_bid,
        'current_bidder': current_bidder,
        'comment_form': comment_form,
        'comments': comments
    }
    return render(request, "auctions/listing.html", context)


def view_categories(request):
    watch_list_counter = WatchList.objects.filter(user=request.user.id).count()


    context = {
        'categories': categories,
        "watchlist_counter": watch_list_counter
    }
    return render(request, "auctions/categories.html", context)


def view_category(request, category_id):
    category = categories[int(category_id)]
    active_listings = AuctionListing.objects.filter(active=True, category=category)
    watch_list_counter = WatchList.objects.filter(user=request.user.id).count()
    context = {"watchlist_counter": watch_list_counter,
               "category": category,
               "active_listings": active_listings}
    return render(request, "auctions/category.html", context)


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
            instance = form.save(commit=False)
            # Check if user entered image url, if not -> assign default image
            if form.cleaned_data['image_url'] is None:
                no_image = 'https://vcunited.club/wp-content/uploads/2020/01/No-image-available-2.jpg'
                instance.image_url = no_image
            instance.user = request.user
            instance.save()
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
