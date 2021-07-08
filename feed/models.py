from datetime import datetime
from time import mktime
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import make_aware, now

from .services import get_valid_feed




class FeedManager(models.Manager):
    def create_feed(self, link):
        """Create a new feed from a link and update this feed articles"""

        feed = get_valid_feed(link)
        feed_obj, _ = self.get_or_create(title=feed['feed'].get('title', 'No title'),
                               subtitle=feed['feed'].get('subtitle', 'No subtitle'),
                               link=link)
        self.update_feed_content(feed_obj, articles=feed['entries'])
        return feed_obj

    def update_feed_content(self, feed, articles=None):
        """Add new articles for the provided feed and return them"""

        # Parse the articles if they are not provided
        if articles is None:
            parsed_feed = get_valid_feed(feed.link)
            articles = parsed_feed['entries']

        articles_obj = []
        for article in articles:
            struct = article['published_parsed']
            dt_created = make_aware(datetime.fromtimestamp(mktime(struct)))
            # Create new articles if does not exist
            article_obj, created = Article.objects.get_or_create(title=article['title'],
                                                                 feed=feed,
                                                                 created=dt_created)
            if created:
                articles_obj.append(article_obj)
        return articles_obj # Return new articles


class Feed(models.Model):
    """Feed is a collection of Articles from one source coming from the provided link"""

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=150, default='No subtitle')
    link = models.URLField(max_length=200, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    objects = FeedManager()

    def __str__(self):
        return self.title

class Article(models.Model):
    """Article is a peace of news from a feed"""

    title = models.CharField(max_length=200)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    created = models.DateTimeField(default=now, blank=False)
    is_read_by = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title
        