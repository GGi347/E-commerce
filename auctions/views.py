from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from auctions.forms import AuctionForm
from .models import Auction_listing, User, Watchlist


def index(request):
    items = Auction_listing.objects.all()
    return render(request, "auctions/index.html", {
        "items": items,
        "header": "Active"
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

@login_required
def create_listing(request):
    if request.method == "POST":
        name = request.POST["name"]
        price = request.POST["price"]
        description = request.POST["description"]
        imageUrl = request.POST["imageUrl"]
        owner = request.user
        item = Auction_listing.objects.create(name=name, price=price, description=description, imageUrl=imageUrl, owner=owner)
        item.save()
    return render(request, "auctions/create_listing.html", {
        "form": AuctionForm()
    })

def item(request, item_id):
    item = Auction_listing.objects.get(pk=item_id)
    watch_item = Watchlist.objects.all()
    print(watch_item)
    return render(request, "auctions/item.html", {
        "item": item,
        "watch_item": watch_item
    })

@login_required
def watchlist(request, item_id):
    item = Auction_listing.objects.get(pk=item_id)
    user = request.user
    watch_item = Watchlist.objects.filter(item=item, user=user)
    if watch_item:
        print("delete")
        watch_item.delete()
    else:
        print("add")
        item_to_add = Watchlist.objects.create()
        item_to_add.save()
        item_to_add.item.add(item)
        item_to_add.user.add(user)
        print("item to add ",item_to_add.item.all())
    
    return HttpResponseRedirect(reverse("item", args=(item.id,) ))


def show_watchlist(request, user_id):
    user = User.objects.filter(pk=user_id)
    wl = Watchlist.objects.filter(user=user)
    print(wl)
    # wl = list(user.wishlist.all())
    # for w in wl:
    #     print(w.item.all())
    
    
        
    # objects = wl.item.all()
    # for w in wl:
    #     print(type(w.item))
    # witems = Watchlist.objects.all()
    # items = []
    # for witem in witems:
    #     items.append(witem.item)

    return render(request, "auctions/watchlist.html", {
        "items": wl,
        "header": "WatchList"
    })