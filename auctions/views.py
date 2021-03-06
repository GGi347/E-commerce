from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from auctions.forms import AuctionForm
from .models import Auction_listing, Comments, User, Watchlist, Bids, Category
from django.contrib import messages

# the home page that shows active listings 
def index(request):
    all_items = Auction_listing.objects.all()
    items = []
    categories = list(Category.objects.all())

    for item in all_items:       
        if item.bidOpen:
            items.append(item)
    return render(request, "auctions/index.html", {
        "items": items,
        "categories": categories,
        "header": "Active",
        "category": "All",
    })


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

# users create new listings. New listings are always set to active by default.
@login_required
def create_listing(request):
    if request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        short_description = request.POST["short_description"]
        long_description = request.POST["long_description"]
        imageUrl = request.POST["imageUrl"]
        owner = request.user
        item = Auction_listing.objects.create(name=name, price=price, short_description=short_description, long_description=long_description, imageUrl=imageUrl, owner=owner)
        item.save()
        # after adding new item, redirected to home index page
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html", {
        "form": AuctionForm()
    })

    
# winner of the bid and the max_bid 
def get_max_bid(item):
    bids = list(Bids.objects.filter(item=item.id))       
    max_bid = item.price
    winner = item.owner
    for bid in bids:
        bid_price = bid.price
        if bid_price > max_bid:
            max_bid = bid_price
            winner = bid.bidder

    return (max_bid, winner)

# shows individual item in detail. also has options for registered users to bid and add to wishlist.
def item(request, item_id):
    item = Auction_listing.objects.get(pk=item_id)
    bids= Bids.objects.filter(item=item_id).count() 
    comments = list(Comments.objects.filter(item=item_id))
    is_watch_item = list(Watchlist.objects.filter(user=request.user.id, item=item_id))
    is_owner = True if item.owner == request.user else False
    # get_max_bid function to get maximum bidding made so far
    max_bid = get_max_bid(item)[0]
    return render(request, "auctions/item.html", {
        "item": item,
        "is_watch_item": is_watch_item,
        "bids": bids,
        "comments": comments,
        "is_owner": is_owner,
        "max_bid": max_bid,
    })

# wishlist of active items or remove items from wishlist
@login_required
def watchlist(request, item_id):
    user = request.user
    item = Auction_listing.objects.get(pk=item_id)
    watch_item = Watchlist.objects.filter(item=item_id, user=user.id)
    if watch_item:
        watch_item.delete()
        messages.add_message(request, messages.INFO, f'Item deleted from the wishlist.')
    else:
        messages.add_message(request, messages.INFO, f'Item added to the wishlist.')
        item_to_add = Watchlist.objects.create(item= item, user=user)
        item_to_add.save()   
    return HttpResponseRedirect(reverse("item", args=(item_id,) ))


def show_watchlist(request):
    user_id = request.user.id
    wish_items = list(Watchlist.objects.filter(user=user_id))
    items = []
    for wish_item in wish_items:
        print(wish_item.item)
        item = Auction_listing.objects.get(pk=wish_item.item.id)
        items.append(item)

    return render(request, "auctions/index.html", {
        "items": items,
        "header": "WatchList"
    })

# items that are closed for bidding.
def closed_listing(request):
    all_items = Auction_listing.objects.all()
    items = []
    for item in all_items:       
        if not item.bidOpen:
            items.append(item)
    return render(request, "auctions/index.html", {
        "items": items,
        "header": "Closed"
    })


@login_required
def place_bid(request, item_id):
    if request.method == "POST":
        item = Auction_listing.objects.get(pk=item_id)
        # get the current maximum bid
        max_bid = get_max_bid(item)[0]
        curr_bid = float(request.POST["bid-amount"])
        # allow to place bid only if the bid is more than current maximum bid
        if curr_bid < max_bid:
            messages.add_message(request, messages.INFO, f'Please place a bid higher than Rs.{max_bid}')
            return HttpResponseRedirect(reverse("item", args=(item_id, )))
        else:
            new_bid = Bids.objects.create(item=item, price=curr_bid, bidder=request.user)
            new_bid.save()
    return HttpResponseRedirect(reverse("item", args=(item_id, )))


@login_required
def close_bid(request, item_id):
    item = Auction_listing.objects.get(pk=item_id)
    item.bidOpen = False
    # get winner of bid
    winner = get_max_bid(item)[1]
    item.winner = winner
    item.save()
    messages.add_message(request, messages.INFO, "The bid has been closed.")
    return HttpResponseRedirect(reverse("item", args=(item_id, )))

# adds comments by users for items
@login_required
def add_comment(request, item_id):
    if request.method == "POST":
        item = Auction_listing.objects.get(pk=item_id)
        comment = request.POST["comment"]
        new_comment = Comments.objects.create(comment=comment, user=request.user, item=item)
        new_comment.save()
    return HttpResponseRedirect(reverse("item", args=(item_id, )))

# lists the available categories in index page. 
def category_listing(request, category_id):
    category = Category.objects.get(pk=category_id)
    categories = Category.objects.all()
    # show all listings if category is all
    if (category.name) == "All":
        all_items = Auction_listing.objects.all()
    else:
        all_items = category.item.all()
    items = []
    for i in all_items:
        item = Auction_listing.objects.get(pk=i.id)
        # show only active listings
        if item.bidOpen:
            items.append(item)
    return render(request, "auctions/index.html", {
        "items": items,
        "category": category.name,
        "categories": categories,
        "header": "Active",
    })