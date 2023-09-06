from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from .models import User, Listing, Bid, Comment

# forms


class ListingForm(ModelForm):
    # missing bid and publisher
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image',
                  'category', 'starting_bid']
        exclude = ['publisher', 'buyer']


def index(request):
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
    if request.method == 'POST':
        form = ListingForm(request.POST)
        listing = form.save(commit=False)
        listing.publisher = request.user
        listing.save()
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data)
    return render(request, "auctions/create.html",
                  {"form": ListingForm()})


def item(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    return render(request, "auctions/item.html", {
        "item": item
    })


def watchlist(request):
    item = User.objects.get(watchlist)
    print(item)
    return render(request, "auctions/watchlist.html")
