from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True)

    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    title = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.title}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    image = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    starting_bid = models.PositiveIntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="purchased")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    publisher = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, related_name="myListings")
    watchlist = models.ManyToManyField(
        User, blank=True, null=True, related_name="myWatchlist")

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=300)
    publisher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"on '{self.listing}', {self.publisher} said: {self.message}"


class Bid(models.Model):
    amount = models.PositiveIntegerField(default=0)
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="myBid")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, null=True, related_name="allBids")
    date_created = models.DateField(default=datetime.now)

    def __str__(self):
        return f"{self.bidder} bid {self.amount}"
