from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *

def create_listing(request):
    # return HttpResponse('hello')
    if request.method=="POST":
        user=request.user
        title=request.POST["title"]
        description=request.POST['Description']
        image_url=request.POST['image_url']
        category=request.POST['category']
        # bid=request.POST['bid']
        bid1 = Bid(bid=int(request.POST["bid"]), user=user)
        bid1.save()
        listing=Listing(title=title,description=description,owner=user,category=category,url=image_url,bid=bid1)
        listing.save()
        # return HttpResponseRedirect(reverse("index"))
        return render(request,"auctions/index.html",{
            "listings":Listing.objects.all()
        })
    else:
        return render(request,"auctions/create_listing.html")
def display_listing(request, listing_id):
    # listing=Listing.objects.get(pk=listing_id)
    # # is_owner = request.user.username == listing.owner.username
    # return render(request,"auctions/listing.html",{
    #     "listing":listing,
    #     # "owner":is_owner
    #     "is_listing_in_watchlist":request.user in listing.watchlist.all()
    # })
    listing = Listing.objects.get(pk=listing_id)
    # comments=Comment.objects.get(pk=listing_id)
    # is_listing_in_watchlist = request.user  in 
    # x=listing.watchlist.all()
    is_listing_in_watchlist = request.user.username  == listing.watchlist
    comments = listing.comments.all()
    is_owner = request.user.get_username() 
    is_owner1=listing.owner
    context = {
        "listing": listing,
        "is_listing_in_watchlist": is_listing_in_watchlist,
        "is_owner": is_owner,
        "comments":comments,
        "is_owner1":is_owner1
    }
    return render(request, "auctions/listing.html", context)
def select_list(request):
    if(request.method=="POST"):
        category1 = request.POST["category"]
        listings= Listing.objects.filter(category=category1)
        context = {
        "listings": listings,
        }
        return render(request, "auctions/index.html", context)
    else:
        return HttpResponse("Not found")
    
def new_bid(request, listing_id):
      listing = Listing.objects.get(pk=listing_id)
      current_bid = listing.bid.bid
      new_bid = int(request.POST["bid"])
      if new_bid > current_bid:
           updated_bid = Bid(bid=new_bid, user=request.user)
           updated_bid.save()
           listing.bid = updated_bid
           listing.save()
           is_owner = request.user.get_username() 
           is_owner1=listing.owner
           return render(request, "auctions/listing.html", {
               "listing": listing,
               "message": "Bid was updated successfully",
               "updated": True,
               "is_owner": is_owner,
               "is_owner1":is_owner1
            })
      else:
           return render(request, "auctions/listing.html", {
               "listing": listing,
               "message": "Bid not high enough",
               "updated": False,
            })
def comment(request, listing_id):
    comment=request.POST["comment"]
    writer=request.user
    listing=Listing.objects.get(pk=listing_id)
    com=Comment(comment=comment,writer=writer,listing=listing)
    com.save()
    return HttpResponseRedirect(reverse("display_listing", args=(listing_id, )))
def add_watchlist(request, listing_id):
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        # user=request.user.username
        # listing=Listing(watchlist=user)
        # listing.watchlist.set()
        listing.watchlist.add(request.user.username)
        # listing.save()
        # listing.watchlist+=request.user.username
        listing.save()
        return HttpResponseRedirect(reverse("display_listing", args=(listing_id, )))
    # listing=Listing.objects.get(pk=listing_id)
    # writer=request.user
    # com=watchlist(watch_list=writer,listing=listing)
    
def index(request):
        return render(request,"auctions/index.html",{
            "listings":Listing.objects.all(),
        })
    # return render(request, "auctions/index.html")

def close_auction(request,listing_id):
    listing=Listing.objects.get(pk=listing_id)
    listing.is_closed=True
    listing.save()
    return HttpResponseRedirect(reverse("display_listing", args=(listing_id, )))
def closed_list(request):
    return render(request,"auctions/closed_listing.html",{
                    "listings":Listing.objects.all(),
    })
def check_product(request, listing_id):
    return render(request,"auctions/check_product.html",{
                    "listings":Listing.objects.get(pk=listing_id),
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