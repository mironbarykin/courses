from podcaster.models import Episode, Podcast


def process(question: str) -> tuple:
    """
    Returning the search result, by question argument,
    ('episode'/'podcast'/'index', search_result)
    """
    suitable_episodes = Episode.objects.filter(name__icontains=question)
    suitable_podcasts = Podcast.objects.filter(name__icontains=question)
    # Check if results more than one
    if len(suitable_podcasts) + len(suitable_episodes) == 1:
        if len(suitable_episodes) == 1:
            return 'episode', {'id': suitable_episodes[0].id}
        else:
            return 'podcast', {'id': suitable_podcasts[0].id}
    return 'index', {'podcasts': suitable_podcasts, 'episodes': suitable_episodes}
