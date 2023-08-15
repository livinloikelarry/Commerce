from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ForeignKey(
        'Listing', on_delete=models.SET_NULL,  null=True)


CATEGORY_CHOICES = (
    ("APPAREL", "Apparel"),
    ("ELECTRONICS", "Electronics"),
    ("ENTERTAINMENT", "Entertainment"),
    ("HOBBIES", "Hobbies"),
    ("HOME", "Home"),
    ("TOYS/GAMES", "Toys/Games"),
    ("INSTRUMENTS", "Instruments"),
    ("UNKNOWN", "Unknown")
)


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    bid = models.ForeignKey('Bid', on_delete=models.SET_NULL, null=True)
    image = models.URLField()
    is_active = models.BooleanField()
    publisher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    comments = models.ForeignKey(
        'Comment', on_delete=models.SET_NULL, null=True)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='UNKNOWN'
    )


class Comment(models.Model):
    message = models.CharField(max_length=300)
    publisher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")


class Bid(models.Model):
    amount = models.PositiveIntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
