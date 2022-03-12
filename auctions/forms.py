
from .models import Auction_listing
from django import forms

class AuctionForm(forms.ModelForm):
     class Meta:
        model = Auction_listing
        exclude = ['owner']
