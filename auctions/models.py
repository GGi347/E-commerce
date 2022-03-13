from email.policy import default
from unicodedata import name
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction_listing(models.Model):
    name = models.CharField(max_length=120)
    price = models.FloatField()
    description = models.CharField(max_length=500, blank=True)
    createdDate = models.DateTimeField(auto_now=True)
    imageUrl = models.CharField(null=True, blank=True, max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    bidOpen = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="winner")


class Bids(models.Model):
    item = models.ForeignKey(Auction_listing, on_delete=models.CASCADE)
    price = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    biddingDate = models.DateTimeField(auto_now=True)
    

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    commentDate = models.DateTimeField(auto_now=True)
    item = models.ForeignKey(Auction_listing, on_delete=models.CASCADE)

class Watchlist(models.Model):
    item = models.ForeignKey(Auction_listing,  default=1, on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    added_on = models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=40)
    item = models.ManyToManyField(Auction_listing, related_name="item")
    