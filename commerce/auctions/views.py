from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import *

class NewAuctionForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description", widget=forms.Textarea)
    starting_bid = forms.IntegerField(label="Starting Bid", min_value=1)
    img_url = forms.URLField(label="Image URL (Optional)", required=False)

def index(request):
    auctions_list = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "auctions_list": auctions_list
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

def add(request):
    if request.method == "POST":
        if 'title' in request.POST:
            title = request.POST['title']
            description = request.POST['description']
            starting_bid = request.POST['starting_bid']
            img_url = request.POST['img_url']

            user = request.user
            
            if img_url:
                auction_item = Auction(user=user, title=title, description=description, starting_bid=starting_bid, img_url=img_url)
            else:
                auction_item = Auction(user=user, title=title, description=description, starting_bid=starting_bid)
            auction_item.save()
            print(auction_item)

    return render(request, "auctions/add.html", {
        "form": NewAuctionForm()
    })

def item_view(request, auction_id):
    item = Auction.objects.get(pk=auction_id)
    bids = Bid.objects.filter(pk=auction_id)

    highest_bid = item.starting_bid
    if bids:
        highest_bid = max(highest_bid, max(bids))
        
    return render(request, "auctions/item.html", {
        "item": item,
        "highest_bid": highest_bid,
    })