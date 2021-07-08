import pytest
from feed.models import Feed, Article


@pytest.fixture
def feed(user):
    feed = Feed.objects.create_feed('http://www.nu.nl/rss/Algemeen')
    
    feed.subscribers.add(user)
    return feed


@pytest.fixture
def another_feed():
    feed = Feed.objects.create_feed('https://feeds.feedburner.com/tweakers/mixed')
    return feed


@pytest.fixture
def article(user, feed):
    article = Article.objects.create(title = 'Artcile1 test title', 
                                     feed = feed)
    article.is_read_by.set([user])
    return article


@pytest.fixture
def another_article(another_feed):
    article = Article.objects.create(title = 'Artcile2 test title', 
                                     feed = another_feed)
    return article
