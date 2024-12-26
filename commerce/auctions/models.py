from django.contrib.auth.models import AbstractUser
from django.db import models
    

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Auction(models.Model):
    creater = models.ForeignKey(User, models.CASCADE, related_name="auctioneer")
    title = models.CharField(max_length=64)
    description = models.TextField()
    highest_bid = models.IntegerField()
    img_url = models.URLField(blank=True, default="https://github.com/joanne5548/cs50-projects/blob/main/commerce/auctions/static/auctions/assets/default_image.png?raw=true")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, models.CASCADE, related_name="item_winner", blank=True, null=True)
    # closing_bid = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}"
        # return f"Title: {self.title}\nDescription: {self.description}\nFor ${self.starting_bid} with image: {self.img_url}"

class Bid(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="bidder")
    item = models.ForeignKey(Auction, models.CASCADE, related_name="bid_item")
    amount = models.IntegerField()

    def __str__(self):
        return f"Bid: ${self.amount} by {self.user}"

class Comment(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="commenter")
    content = models.CharField(max_length=512)
    item = models.ForeignKey(Auction, models.CASCADE, related_name="comment_item")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content}"