from rest_framework import viewsets
from .models import Feed, Article
from .serializers import FeedSerializer, ArticleSerializer


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    """Feed endpoint to get one or all feeds"""
    
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """ Article endpoint to get one or all artcles for the selected feed"""

    # Get articles for only selected feed
    def get_queryset(self):
        return Article.objects.filter(feed=self.kwargs['feed_pk'])
    serializer_class = ArticleSerializer
    
