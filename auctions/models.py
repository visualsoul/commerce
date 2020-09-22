from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    CATEGORY = (
        ("Laptop", "Laptop"),
        ("Desktop PC", "Desktop PC"),
        ("CPU", "CPU"),
        ("Memory (RAM)", "Memory (RAM)"),
        ("Motherboards", "Motherboards"),
        ("Graphics Cards", "Graphics Cards"),
        ("Networking", "Networking"),
        ("Audio", "Audio"),
        ("Other Components", "Other Components"),
    )
    # AuctionListing needs User id -> we need to know who posted the Listing -> onetomany? one user can have several listings
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    starting_bid = models.FloatField(null=True)
    current_bid = models.FloatField(null=True, default=0)
    image_url = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    active = None  # Should be True or False if Listing Closed active should be False

    def __str__(self):
        return f'{self.title}, Posted by: {self.user}'


class Bid(models.Model):
    # bid needs amount
    amount = models.FloatField()
    # bid needs bidder - User id (FK)
    bidder = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # bid needs datetime timestamp
    dt = models.DateTimeField(auto_now_add=True)
    # bid needs AuctionListing id -> we need to know which user.id is bidding on which AuctionListing.id manytomany?
    listing = models.ForeignKey(AuctionListing, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.listing}, Highest Bidder: {self.bidder}, Offer: ${self.amount:,.2f}"


class Comment(models.Model):
    # comment needs User id  (FK)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # comment needs datetime stamp
    dt = models.DateTimeField(auto_now_add=True)
    # comment needs message
    message = models.CharField(max_length=200, null=True)
    # comment needs AuctionListing ID  (FK)
    listing = models.ForeignKey(AuctionListing, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.listing}, {self.dt}: {self.message}"


class WatchList(models.Model):
    is_watching = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} is watching: {self.listing}"