from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    

    def __str__(self):
        return f"{self.title} - {self.starting_bid}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount}"
    
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return f"{self.comment}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"{self.user} - {self.listing}"


class Winner(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="winner")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner")

    def __str__(self):
        return f"{self.user} - {self.listing}"

class Closed(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="closed")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="closed")

    def __str__(self):
        return f"{self.user} - {self.listing}"
    
    
class CategoryListing(models.Model):
    category_ref = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_listings")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="category_listings")

    def __str__(self):
        return f"{self.category} - {self.listing}"
    
class Auction(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="auction")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    winner = models.ForeignKey(Winner, on_delete=models.CASCADE, related_name="auction")
    closed = models.ForeignKey(Closed, on_delete=models.CASCADE, related_name="auction")

    def __str__(self):
        return f"{self.listing} - {self.bid} - {self.winner} - {self.closed}"