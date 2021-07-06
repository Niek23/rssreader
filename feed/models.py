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

        feed_obj = self.create(name=feed['feed']['title'], link=link)
        self.update_feed_content(feed_obj, articles=feed['entries'])

        return feed_obj
    
    def update_feed_content(self, feed, articles=None):
        """Adds new articles for the provided feed"""

        # Parse the articles if they are not provided
        if articles is None:
            import feedparser
            articles = feedparser.parse(feed.link)['entries']
        
        # Create new articles if do not exist
        for article in articles:
            Article.objects.get_or_create(title=article['title'], feed=feed)



class Feed(models.Model):
    """Feed os a collection of Articles from one source coming from link"""

    name = models.CharField(max_length=100, unique=True)
    link = models.URLField(max_length=200, unique=True)

    objects = FeedManager()

    def __str__(self):
        return self.name

class Article(models.Model):
    """Article is a peace of news from a feed"""

    title = models.CharField(max_length=200, unique=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    


