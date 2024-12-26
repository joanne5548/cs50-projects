from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import *

class NewAuctionForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description", widget=forms.Textarea)
    starting_bid = forms.IntegerField(label="Starting Bid", min_value=1)
    img_url = forms.URLField(label="Image URL (Optional)", required=False)

class NewBidForm(forms.Form):
    def __init__(self, highest_bid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bid_amount'] = forms.IntegerField(label="New Bid", min_value=highest_bid)

class NewCommentForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea)

def index(request):
    return render(request, "auctions/index.html", {
        "auctions_list": Auction.objects.filter(active=True)
    })

def closed(request):
    return render(request, "auctions/closed.html", {
        "closed_items": Auction.objects.filter(active=False)
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
        form = NewAuctionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            img_url = form.cleaned_data['img_url']

            user = request.user
            
            if img_url:
                auction_item = Auction(creater=user, title=title, description=description, highest_bid=starting_bid, img_url=img_url)
            else:
                auction_item = Auction(creater=user, title=title, description=description, highest_bid=starting_bid)
            auction_item.save()

            return redirect('item', auction_item.id)
        else:
            return render(request, "auctions/add.html", {
                "form": form
            })

    return render(request, "auctions/add.html", {
        "form": NewAuctionForm()
    })

# def get_highest_bid(current_highest_bid, auction_id):
#     bids_amount_list = Bid.objects.filter(item=auction_id).values_list('amount', flat=True)

#     highest_bid = current_highest_bid
#     if bids_amount_list:
#         highest_bid = max(current_highest_bid, max(bids_amount_list))
    
#     return highest_bid

def handle_new_bid(item, highest_bid, request):
    bid_form = NewBidForm(highest_bid, request.POST)
    if bid_form.is_valid():
        new_bid_amount = bid_form.cleaned_data['bid_amount']
        if new_bid_amount > highest_bid:
            bid = Bid(user=request.user, item=item, amount=new_bid_amount)
            bid.save()
            item.highest_bid = new_bid_amount
            item.save()
            return render(request, "auctions/item.html", {
                "item": item,
                "highest_bid": new_bid_amount,
                "bid_form": NewBidForm(new_bid_amount),
                "comment_form": NewCommentForm(),
            })
        
    return render(request, "auctions/item.html", {
        "item": item,
        "highest_bid": highest_bid,
        "bid_form": bid_form,
        "message": "Please bid higher than the current bid."
    })

def handle_close_bid(item, request):
    item.active = False
    item.winner = request.user
    item.save()

    return render(request, "auctions/item.html", {
        "item": item,
        "highest_bid": item.highest_bid
    })

def item_view(request, auction_id):
    item = Auction.objects.get(pk=auction_id)
    highest_bid = item.highest_bid #get_highest_bid(item.highest_bid, auction_id)

    if request.method == 'POST':
        if 'close_bid' in request.POST:
            return handle_close_bid(item, request)
        elif 'content' in request.POST:
            comment_form = NewCommentForm(request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data['content']
                comment = Comment(user=request.user, content=content, item=item)
                comment.save()
        else:
            return handle_new_bid(item, highest_bid, request)

    return render(request, "auctions/item.html", {
        "item": item,
        "highest_bid": highest_bid,
        "bid_form": NewBidForm(highest_bid),
        "comment_form": NewCommentForm(),
        "comments_list": Comment.objects.filter(item=auction_id)
    })