from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response 
from .serializers import FeedSerializer, ArticleSerializer
from .services import subscribe_to_feed, mark_article_read, filter_read
from .models import Feed, Article



class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    """Feeds endpoint to get one or all feeds and (un)subscribe to the selected one"""

    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    @action(methods=['get'], detail=True, url_path='subscribe')
    def subscribe(self, request, pk=None):
        """Feed endpoint to subscribe the user to the feed"""
        return subscribe_to_feed(request.user, self.get_object())

    @action(methods=['get'], detail=True, url_path='unsubscribe')
    def unsubscribe(self, request, pk=None):
        """Feed endpoint to unsubscribe the user from the feed"""
        return subscribe_to_feed(request.user, self.get_object(), subsrcibe=False)
    
    @action(methods=['get'], detail=True, url_path='update-articles')
    def update_articles(self, request, pk=None):
        """Feed endpoint to load new articles"""
        new_articles = Feed.objects.update_feed_content(self.get_object())
        return Response({'new_enries': ArticleSerializer(new_articles, many=True).data})


class MyFeedViewSet(viewsets.ReadOnlyModelViewSet):
    """ Feeds endpoint to get a list of feeds a user subcribed to"""

    queryset = Feed.objects.all()
    def get_queryset(self):                                    
        return super().get_queryset().filter(subscribers__id=self.request.user.id)
    serializer_class = FeedSerializer




class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """ Article endpoint to get one or all artcles for the selected feed"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        # Filter per feed and read/unread based on read paramenter in url
        read = self.request.query_params.get('read')
        qs = super().get_queryset().filter(feed=self.kwargs['feed_pk'])
        return filter_read(qs, read, self.request)
        
    @action(methods=['get'], detail=True, url_path='mark-read')
    def mark_read(self, request, pk=None, feed_pk=None):
        """Endpoint to mark an article as read"""
        return mark_article_read(request.user, self.get_object())
    
    @action(methods=['get'], detail=True, url_path='unmark-read')
    def unmark_read(self, request, pk=None, feed_pk=None):
        """Endpoint to unmark an article as read"""
        return mark_article_read(request.user, self.get_object(), mark=False)





