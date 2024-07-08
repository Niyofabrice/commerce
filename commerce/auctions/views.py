from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *



def index(request):
    listings = Listing.objects.filter(closed=False)
    context = {
        "listings": listings,
    }
    return render(request, "auctions/index.html", context)


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
    messages.success(request, "Logged out")
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
        messages.success(request, "Account created successfully!")
        return HttpResponseRedirect(reverse("index"))
    else:
        messages.error(request, "An error occurred. Please try again.")
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        category = request.POST["category"]
        image_url = request.POST["image_url"]
        user = request.user

        new_listing = Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            category=Category.objects.get(name=category),
            image_url=image_url,
            seller=user
        )
        new_listing.save()
        messages.success(request, "Listing created successfully!")
        return HttpResponseRedirect(reverse("index"))
    context = {
        "categories": Category.objects.all()
    }
    messages.error(request, "An error occurred. Please try again.")
    return render(request, "auctions/create_listing.html", context)


@login_required(login_url="login")
def create_category(request):
    if request.method == "POST":
        name = request.POST["name"]
        new_category = Category(name=name)
        new_category.save()
        return HttpResponseRedirect(reverse("create_listing"))
    return render(request, "auctions/create_category.html")

def listing(request, listing_id):
    winner = None
    comments = None
    watchlist = None

    listing = Listing.objects.get(pk=listing_id)
    bids = listing.bids.all()
    top_bid = listing.bids.order_by("-amount").first()
    try:
        comments = Comment.objects.filter(listing=listing)
    except Comment.DoesNotExist:
        comments = None
    
    try:
        winner = Winner.objects.filter(listing=listing).first()
    except Winner.DoesNotExist:
        winner = None
    
    try:
        watchlist = listing.watchlist.all().filter(user=request.user)
    except Watchlist.DoesNotExist:
        watchlist = None

    context = {
        "listing": listing,
        "comments": comments,
        "total_bids": bids.count(),
        "top_bid": top_bid,
        "winner": winner,
        "watchlist": watchlist
    }
    return render(request, "auctions/listing.html", context)


def add_comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        comment = request.POST["comment"]
        new_comment = Comment(
            author=user,
            listing=listing,
            comment=comment
        )
        new_comment.save()
        messages.success(request, "Comment posted successfully!")
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))



def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        bid_amount = float(request.POST["bid"])
        bids = Bid.objects.filter(listing=listing)
        print(bids)
        if bids:
            current_top_bid = listing.bids.order_by("-amount").first()
            if bid_amount <= listing.starting_bid or bid_amount <= current_top_bid:
                messages.error(request, "Your bid is lower than the starting bid or the current highest bid")
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        if bid_amount <= listing.starting_bid:
            messages.error(request, "Your bid is lower than the starting bid")
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        new_bid = Bid(
            listing=listing,
            user=user,
            amount=bid_amount
        )
        new_bid.save()
        messages.success(request, "Your bid has been successfully placed!")
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    

def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        watchlist, created = Watchlist.objects.get_or_create(user=user)
        watchlist.listing.add(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def remove_from_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        watchlist = Watchlist.objects.get(user=user)
        watchlist.listing.remove(listing)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


  
def watchlist(request):
    user = request.user
    try:
        watchlist = Watchlist.objects.get(user=user)
        listings = watchlist.listing.all()
    except Watchlist.DoesNotExist:
        listings = []  # If the watchlist does not exist, set listings to an empty list
    context = {
        "watchlist": listings
    }
    return render(request, "auctions/watchlist.html", context)


def categories(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, "auctions/categories.html", context)

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = category.listings.all()
    context = {
        "category": category,
        "listings": listings
    }
    return render(request, "auctions/category.html", context)

def close_auction(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        top_bid = listing.bids.order_by("-amount").first()
        if top_bid:
            user = top_bid.user
            winner = Winner(
                listing=listing,
                user=user
            )
            winner.save()
        listing.closed = True
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))