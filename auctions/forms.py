from django.forms import ModelForm
from django import forms

from .models import *

class CreateListing(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'category', 'image_url']


class PlaceBid(forms.Form):
     amount = forms.FloatField(label='Bid')


class CommentForm(forms.Form):
    message = forms.CharField(label="Comment", max_length=200, widget=forms.Textarea(attrs={'class': "form-control comment-form"}))


