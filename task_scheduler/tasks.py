import dramatiq
from feed.models import Feed
from .scheduler import cron


@cron("* * * * *")
@dramatiq.actor
def update_feeds():
    """Updates articles for all stored feeds"""
    feeds = Feed.objects.all()
    for feed in feeds:
        new_entires = Feed.objects.update_feed_content(feed)
        print(f'Feed * {feed.title} * has been updated with {len(new_entires)} new entries')
