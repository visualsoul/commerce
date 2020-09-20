from django.contrib import admin
from . models import User, AuctionListing, Comment, Bid, WatchList
# Register your models here.

admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(WatchList)