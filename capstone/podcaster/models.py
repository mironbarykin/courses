from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Model of user includes: 
        username
        password
        email
        age
        country
    Model of users is related to:
        podcasts ('author' PODCAST)
        subscriptions ('subscribers' PODCAST)
        queue ('queuned_users' EPISODE)
        liked_on ('liked_by' EPISODE)
        comments ('author' COMMENT)
    Model of user have functions:
        is_author respond with 'True' when user has podcasts and 'False' when hasn't
    """
    age = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)

    def is_author(self) -> bool:
        try:
            podcasts = self.podcasts
            return True
        except:
            return False


class Podcast(models.Model):
    """
    Model of podcast includes: 
        name (of this podcast)
        description (of this podcast) 
        image (url of podcast's image) 
        date (when podcast was created)
        author (who was created this podcast)
        subscribers (who subscribed on this podcast)
    Model of podcast is related to:
        episodes ('podcast' EPISODE)
    """
    name = models.CharField(max_length=256)
    description = models.TextField()
    image = models.URLField(max_length=256)
    date = models.DateField()
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='podcasts')
    subscribers = models.ManyToManyField(User, related_name='subscriptions', blank=True, null=True)


class Episode(models.Model):
    """
    Model of episode includes: 
        podcast (in which episode was published) 
        name (of this episode)
        description (of this episode) 
        image (url of episode's image) 
        audio (file of episode)
        timetags (might be none, tage like "00:00 TAG_DESCRIPTION")
        date (when episode was published)
        liked_by (who liked this episode)
        queuned_users (who is put this episode to queue)
    Model of episode is related to:
        comments ('episode' COMMENT)
    """
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='episodes')
    name = models.CharField(max_length=256)
    description = models.TextField()
    image = models.URLField(max_length=256)
    audio = models.FileField(upload_to='episodes')
    timetags = models.TextField(blank=True)
    date = models.DateField()
    liked_by = models.ManyToManyField(User, related_name='liked_on', blank=True, null=True)
    queuned_users = models.ManyToManyField(User, related_name='queue', blank=True, null=True)


class Comment(models.Model):
    """
    Model of comment includes: 
        author (of the comment)
        episode (where comment was published)
        date (when comment was published)
        content (what is the comment content)
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='comments')
    date = models.DateField()
    content = models.TextField()
