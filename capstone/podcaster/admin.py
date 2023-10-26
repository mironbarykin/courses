from django.contrib import admin
from .models import User, Podcast, Episode, Comment

admin.site.register(User)
admin.site.register(Podcast)
admin.site.register(Episode)
admin.site.register(Comment)
