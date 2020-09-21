from django.forms import ModelForm
from django import forms

from .models import *

class CreateListing(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'category', 'image_url']


