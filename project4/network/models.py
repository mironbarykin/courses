from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followings')

    def count_followers(self):
        return self.followers.count()
    
    def count_following(self):
        return User.objects.filter(followers=self).count()

    def serialize(self):
        return {
            "id": self.id,
            "followers": [i.id for i in self.followers.all()],
        }

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=False)
    likedby = models.ManyToManyField(User, blank=True, related_name="likeon")
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "author": {
                "username": self.author.username,
                "id": self.author.id,
            },
            "content": self.content,
            "likes": {
                "users": [i.id for i in self.likedby.all()]
            },
            "timestamp": str(self.timestamp)[:10] + ' ' + str(self.timestamp)[11:16],
        }
