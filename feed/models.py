from django.contrib.auth.models import User
from django.db import models
from django.db.models.expressions import Value



class FeedManager(models.Manager):
    def create_feed(self, link):
        """Creates a new feed from a link and updates this feed articles"""
        
        import feedparser
        feed = feedparser.parse(link)

        # Check is the provided link is a valid rss source
        if feed['entries'] == []:
            raise ValueError('The provided link does not have any rss entries')

        feed_obj = self.create(title=feed['feed']['title'], subtitle=feed['feed']['subtitle'], link=link)
        self.update_feed_content(feed_obj, articles=feed['entries'])

        return feed_obj
    
    def update_feed_content(self, feed, articles=None):
        """Adds new articles for the provided feed and returns new articles"""

        # Parse the articles if they are not provided
        if articles is None:
            import feedparser
            articles = feedparser.parse(feed.link)['entries']
        
        articles_obj = []
        for article in articles:
            # Create new articles if do not exist
            article_obj, created = Article.objects.get_or_create(title=article['title'], feed=feed)
            if created:
                articles_obj.append(article_obj)
        return articles_obj # Return new articles


class Feed(models.Model):
    """Feed os a collection of Articles from one source coming from link"""

    title = models.CharField(max_length=100, unique=True)
    subtitle = models.CharField(max_length=150, default='No subtitle')
    link = models.URLField(max_length=200, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    objects = FeedManager()

    def __str__(self):
        return self.title

class Article(models.Model):
    """Article is a peace of news from a feed"""

    title = models.CharField(max_length=200, unique=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    is_read_by = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title
    


