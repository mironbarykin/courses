from podcaster.models import Episode, Podcast, User


def action(requested_user: User, id: int, requested_action: str) -> None:
    """
    Made action, which provided, on Episode/Podcast with provided id.
    Requesting user also required. Returns None
    """
    if requested_action == 'queue':
        requested_user.queue.add(Episode.objects.get(id=id))
    if requested_action == 'unqueue':
        requested_user.queue.remove(Episode.objects.get(id=id))
    if requested_action == 'like':
        requested_user.liked_on.add(Episode.objects.get(id=id))
    if requested_action == 'unlike':
        requested_user.liked_on.remove(Episode.objects.get(id=id))
    if requested_action == 'subscribe':
        requested_user.subscriptions.add(Podcast.objects.get(id=id))
    if requested_action == 'unsubscribe':
        requested_user.subscriptions.remove(Podcast.objects.get(id=id))
