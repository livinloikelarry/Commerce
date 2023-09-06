from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create_listing"),
    path("category", views.category, name="category_home"),
    path("category/<str:title>/", views.category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("item/<int:listing_id>/", views.item, name="item")
]
