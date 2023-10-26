from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}. Watchlist: {self.watchlist}"


class Listing(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    starting_bid = models.IntegerField()
    image = models.URLField()
    category = models.CharField(max_length=30)
    status = models.CharField(max_length=6, default="active")

    savedby = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.author} posted listing '{self.title}' in {self.category}"
    


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.author} posted comment '{self.content}' in {self.listing}"


class Bid(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.author} posted bid '{self.amount}' in {self.listing}"

