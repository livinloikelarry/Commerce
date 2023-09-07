from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from .models import User, Listing, Bid, Comment, Category


def index(request):
    """ Displays only the listings that are active """

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True)
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


def create(request):
    allCategories = Category.objects.all()
    if request.method == 'GET':
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        category = request.POST["category"]
        publisher = request.user
        price = request.POST["starting_bid"]
        # category info for the category user selected
        category_info = Category.objects.get(title=category)
        # create a new listing
        listing = Listing(
            title=title,
            description=description,
            image=image,
            category=category_info,
            starting_bid=float(price),
            publisher=publisher
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))


def item(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    item_publisher = item.publisher
    comments = Comment.objects.filter(listing=item)
    user = request.user
    listing_in_watchlist = user in item.watchlist.all()
    owner = True if user == item_publisher else False
    winner = True if not item.is_active and item.winner == user else False
    return render(request, "auctions/item.html", {
        "item": item,
        "listing_in_watchlist": listing_in_watchlist,
        "comments": comments,
        "owner": owner,
        'winner': winner
    })


def watchlist(request):
    user = request.user
    items_on_watchlist = Listing.objects.filter(watchlist=user)
    return render(request, "auctions/watchlist.html", {
        "listings": items_on_watchlist
    })


def add_to_watchlist(request, id):
    listing = Listing.objects.get(id=id)
    user = request.user
    # what to do if update not successful
    listing.watchlist.add(user)
    listing.save()
    return HttpResponseRedirect(reverse("item", args=[id]))


def remove_from_watchlist(request, id):
    listing = Listing.objects.get(id=id)
    user = request.user
    # what to do if update not successful
    listing.watchlist.remove(user)
    listing.save()
    return HttpResponseRedirect(reverse("item", args=[id]))


def comment(request, id):
    if request.method == "POST":
        message = request.POST["comment"]
        listing = Listing.objects.get(id=id)
        user = request.user
        comment = Comment(listing=listing, message=message, publisher=user)
        comment.save()
    return HttpResponseRedirect(reverse("item", args=[id]))


def make_bid(request, id):
    if request.method == "POST":
        amount = request.POST["amount"]
        amount = int(amount) if amount.isdigit() else 0
        listing = Listing.objects.get(id=id)
        user = request.user
        if amount > listing.starting_bid:
            listing.starting_bid = amount
            listing.winner = user
            listing.save()
            bid = Bid(amount=amount, bidder=user, listing=listing)
            bid.save()
            return render(request, "auctions/item.html", {
                "item": listing,
                "status": True,
                "update": True
            })
        else:
            return render(request, "auctions/item.html", {
                "item": listing,
                "status": False,
                "update": True
            })


def close_listing(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        listing.is_active = False
        listing.save()
    return HttpResponseRedirect(reverse("item", args=[id]))


def category(request, title=""):
    all_categories = Category.objects.all()
    if title:
        category = Category.objects.get(title=title)
        items_in_selected_category = Listing.objects.filter(
            category=category, is_active=True)
    else:
        items_in_selected_category = None
    return render(request, "auctions/category.html", {
        "categories": all_categories,
        "title": title,
        "listings": items_in_selected_category})
