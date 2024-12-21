from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    starting_bid = models.IntegerField()

class Bid(models.Model):
    name = models.ForeignKey(User, models.CASCADE, related_name="bidder")
    amount = models.IntegerField()

class Comment(models.Model):
    name = models.ForeignKey(User, models.CASCADE, related_name="commenter")
    comment = models.CharField(max_length=512)
    time = models.TimeField(auto_now_add=True)