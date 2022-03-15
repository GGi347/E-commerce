
from logging import PlaceHolder
from .models import Auction_listing
from django import forms

class AuctionForm(forms.ModelForm):
     long_description = forms.CharField(widget=forms.Textarea)
     short_description = forms.CharField(widget=forms.Textarea)
     
     class Meta:
        model = Auction_listing
        
        exclude = ['owner', 'bidOpen', 'winner']
