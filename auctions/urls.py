from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create_listing"),
    path("category", views.category, name="category_home"),
    path("category/<str:title>/", views.category, name="category"),
    path("addToWatchlist/<int:id>/",
         views.add_to_watchlist, name="add_to_watchlist"),
    path("removeFromWatchlist/<int:id>/",
         views.remove_from_watchlist, name="remove_from_watchlist"),
    path("login", views.login_view, name="login"),
    path("comment/<int:id>/", views.comment, name="comment"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("makebid/<int:id>/", views.make_bid, name="make_bid"),
    path("closeListing/<int:id>/", views.close_listing, name="close_listing"),
    path("item/<int:listing_id>/", views.item, name="item")
]
