from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True)

    def __str__(self):
        return f"{self.username}"


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
    image = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    publisher = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, related_name="listings")
    starting_bid = models.PositiveIntegerField(default=0)
    buyer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="purchase")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='UNKNOWN'
    )

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
    amount = models.PositiveIntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.bidder} bid {self.amount}"
