from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, default=None)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", default=None)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount}"
    
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=None)

    def __str__(self):
        return f"{self.comment}"

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ManyToManyField(Listing, related_name="watchlist")

    def __str__(self):
        return f"{self.user} - {self.listing}"


class Winner(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="winner")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner")

    def __str__(self):
        return f"{self.user} - {self.listing}"
    

    