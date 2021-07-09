from urllib.error import URLError
import dramatiq
from feed.models import Feed
from .scheduler import cron
from time import sleep


@cron("* * * * *")
@dramatiq.actor()
def update_feeds():
    """Updates articles for all stored feeds"""

    feeds = Feed.objects.all()

    for feed in feeds:
        print(f'{feed.title} UPDATING - {feed.updating}')
        if not feed.updating:
            continue
        else:
            success = False
            for _ in range(3):
                try:
                    new_entires = Feed.objects.update_feed_content(feed)
                    print(f'Feed * {feed.title} * has been updated with {len(new_entires)} new entries') 
                    success = True
                    break
                except URLError:
                    print('Sleep for 5 sec')
                    sleep(5)
                    continue
            if not success:
                feed.updating = False
                feed.save()
                print(f'{feed.title} - {feed.updating}')
