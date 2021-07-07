import dramatiq 
from .scheduler import cron
from feed.models import Feed


@cron("* * * * *")
@dramatiq.actor
def idempotent_method():
    feeds = Feed.objects.all()
    for feed in feeds:
        new_entires = Feed.objects.update_feed_content(feed)
        print(f'Feed * {feed.title} * has been updated with {len(new_entires)} new entries')