from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("create-category", views.create_category, name="create_category"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("bid/<int:listing_id>/", views.bid, name="bid"),
    path("add-to-watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("single_category/<int:category_id>", views.category, name="single_category"),
    path("close/<int:listing_id>", views.close_auction, name="close_auction"),
    path("comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("remove-from-watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
]
