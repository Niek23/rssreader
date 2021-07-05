from django.db import models

class Feed(models.Model):
    """Feed os a collection of Articles from one source coming from link"""

    name = models.CharField(max_length=100, unique=True)
    link = models.URLField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    """Article is a peace of news from a feed"""

    title = models.CharField(max_length=200, unique=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    


