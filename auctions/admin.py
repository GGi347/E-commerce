from django.contrib import admin
from .models import Auction_listing, User, Bids

# Register your models here.
admin.site.register(Auction_listing)
admin.site.register(User)
admin.site.register(Bids)