from django.forms import ModelForm
from django import forms

from .models import *

class CreateListing(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'category', 'image_url']

        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control"}),
            'starting_bid': forms.NumberInput(attrs={"class": "form-control", "style": "width: 200px;"}),
            'category': forms.Select(attrs={"class": "form-control", "style": "width: 200px;"}),
            'image_url': forms.TextInput(attrs={"class": "form-control"})
        }

        labels = {'starting_bid': 'Sarting bid in USD'}




class PlaceBid(forms.Form):
     #amount = forms.FloatField(label='Bid', widget=forms.FloatField(attrs={"class": "form-group", 'step': "0.05"}))
     amount = forms.DecimalField(label='', decimal_places=2, min_value=0, max_digits=10, widget=forms.NumberInput(attrs={'class': "form-control"}))


class CommentForm(forms.Form):
    message = forms.CharField(label="Comment", max_length=200, widget=forms.Textarea(attrs={'class': "form-control comment-form"}))


