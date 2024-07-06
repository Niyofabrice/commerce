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
]
