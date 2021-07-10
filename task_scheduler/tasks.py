from urllib.error import URLError
import dramatiq
from feed.models import Feed
from .scheduler import cron


@dramatiq.actor
def on_failure(message, error):
    """Updates auto-udpate status for feed if it triggered 3rd time"""
    retries = message.get('options', {}).get('retries', 1)
    args = message.get('args')
    if args and retries >= 3:
        feed_id = args[0]
        feed = Feed.objects.get(id=feed_id)
        feed.updating = False
        feed.save()
        print(f'Togling updating status for feed * {feed.title} * to False')


@dramatiq.actor(max_retries=3)
def update_feed(feed_id):
    """Update one feed with 3 retries"""
    feed = Feed.objects.get(id=feed_id)
    print(f'* {feed.title} * Auto-updating status - {feed.updating}')
    if not feed.updating:
        return

    new_entires = Feed.objects.update_feed_content(feed)
    print(f'Feed * {feed.title} * has been updated with {len(new_entires)} new entries')


@cron('* * * * *')
@dramatiq.actor()
def update_feeds():
    """Updates articles for all stored feeds"""
    feeds = Feed.objects.all()

    for feed in feeds:
        update_feed.send_with_options(args=(feed.id,), on_failure=on_failure)
