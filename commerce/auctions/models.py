from django.contrib.auth.models import AbstractUser
from django.db import models
    

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Auction(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="auctioneer")
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    img_url = models.URLField(blank=True, default="https://i.imgur.com/cu6sM99.png")

    def __str__(self):
        return f"{self.title}"
        # return f"Title: {self.title}\nDescription: {self.description}\nFor ${self.starting_bid} with image: {self.img_url}"

class Bid(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="bidder")
    item = models.ForeignKey(Auction, models.CASCADE, related_name="bid_item")
    amount = models.IntegerField()

    def __str__(self):
        return f"Bid: ${self.amount} by {self.name}"

class Comment(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="commenter")
    comment = models.CharField(max_length=512)
    item = models.ForeignKey(Auction, models.CASCADE, related_name="comment_item")
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} commented at {self.time}:\n{self.comment}"