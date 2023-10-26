import datetime
from podcaster.models import Episode, Podcast, Comment


def posting_episode(request) -> None:
    """
    Posting the episode with giving request, if successful returns None;
    """
    episode = Episode(name=request.POST['name'], description=request.POST['description'],
                      image=request.POST['image'], audio=request.FILES['audio'],
                      date=datetime.datetime.now().strftime("%Y-%m-%d"),
                      podcast=request.user.podcasts)
    episode.save()


def posting_podcast(request) -> None:
    """
    Posting the podcast with giving request, if successful returns None;
    """
    podcast = Podcast(name=request.POST['name'], description=request.POST['description'],
                      image=request.POST['image'], author=request.user,
                      date=datetime.datetime.now().strftime("%Y-%m-%d"))
    podcast.save()


def posting_comment(request, id) -> None:
    """
    Posting the podcast with giving request and episode id, if successful returns None;
    """
    comment = Comment(author=request.user, date=datetime.datetime.now().strftime("%Y-%m-%d"),
                      content=request.POST['content'], episode=Episode.objects.get(id=id))
    comment.save()
