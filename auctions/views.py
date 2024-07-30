from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Category, Listing, Comment, Bid


def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": all_categories
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

def create_listing(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            "categories": all_categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        owner = request.user

        categoryData = Category.objects.get(Category_names=category)

        bid = Bid(offer=float(price), bidder = owner)
        bid.save()

        new_listing = Listing(
            title=title,
            description=description,
            image_url=image_url,
            price=bid, 
            owner=owner,
            category=categoryData)
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    
def filterCategory(request):
    if request.method == "POST":
        if request.POST['category'] == "All":
            return index(request)
        else:
            categoryform = request.POST['category']
            category = Category.objects.get(Category_names=categoryform)
            active_listings = Listing.objects.filter(is_active=True, category=category)
            all_categories = Category.objects.all()
            return render(request, "auctions/index.html", {
                "listings": active_listings,
                "categories": all_categories
            })   
def listing(request, id):
    listing = get_object_or_404(Listing, pk=id)
    listing_in_watchlist = request.user in listing.watchlist.all()
    all_comments = Comment.objects.filter(listing=listing)
    all_bids = Bid.objects.filter(id = id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": listing_in_watchlist,
        "all_comments": all_comments,
        "all_bids": all_bids
    })
@login_required
def addWatchlist(request, id):
    listingdata = Listing.objects.get(pk=id)
    currentuser = request.user
    listingdata.watchlist.add(currentuser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
    
@login_required
def removeWatchlist(request, id):
    listingdata = Listing.objects.get(pk=id)
    currentuser = request.user
    listingdata.watchlist.remove(currentuser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

@login_required
def showWatchlist(request):
    currentuser = request.user
    watchlist = Listing.objects.filter(watchlist=currentuser)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

@login_required
def addComment(request, id):
    if request.method == "POST":
        currentuser = request.user
        listingdata = Listing.objects.get(pk=id)
        message = request.POST["comment"]

        newComment = Comment(
            author = currentuser,
            listing = listingdata,
            comment = message
        )
        newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

@login_required
def addBid(request, id):
    if request.method == "POST":
        newBid = request.POST['newBid']
        currentuser = request.user
        listingdata = Listing.objects.get(pk=id)
        all_comments = Comment.objects.filter(listing=listingdata)
        listing = get_object_or_404(Listing, pk=id)
        listing_in_watchlist = request.user in listing.watchlist.all()
        if listingdata.is_active == True and int(newBid) > listingdata.price.offer:
            updateBid = Bid(bidder = currentuser, offer = newBid)
            updateBid.save()
            listingdata.price = updateBid
            listingdata.save()
            return render(request, "auctions/listing.html", {
                "listing": listingdata,
                "message": "Bid accepted",
                "update": True,
                "all_comments": all_comments,
                "watchlist": listing_in_watchlist,
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listingdata,
                "message": "Bid not accepted",
                "update": False,
                "all_comments": all_comments,
                "watchlist": listing_in_watchlist,
            })