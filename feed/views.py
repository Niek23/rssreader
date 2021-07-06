from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response 
from .models import Feed, Article
from .serializers import FeedSerializer, ArticleSerializer


class FeedViewSet(viewsets.ReadOnlyModelViewSet):
    """Feeds endpoint to get one or all feeds and (un)subscribe to the selected one"""

    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    @action(methods=['get'], detail=True, url_path='subscribe')
    def subscribe(self, request, pk=None):
        """Feed endpoint to subscribe the user to the feed"""
        
        feed = self.get_object()
        user = request.user

        # Check if the user is already subcribed to the feed
        if feed.subscribers.filter(pk = user.id).exists():
            return Response({'message':'You are already subscribed to this feed'})

        feed.subscribers.add(user)
        return Response({'message': f'You have successfully subscribed to {feed} feed'})

    @action(methods=['get'], detail=True, url_path='unsubscribe')
    def unsubscribe(self, request, pk=None):
        """Feed endpoint to unsubscribe the user from the feed"""

        feed = self.get_object()
        user = request.user

        # Check if the user is not subcribed to the feed
        if not feed.subscribers.filter(pk = user.id).exists():
            return Response({'message':'You are not subscribed to this feed'})

        feed.subscribers.remove(user)
        return Response({'message': f'You have successfully unsubscribed from {feed} feed'})

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """ Article endpoint to get one or all artcles for the selected feed"""

    # Get articles for only selected feed
    def get_queryset(self):
        return Article.objects.filter(feed=self.kwargs['feed_pk'])
    serializer_class = ArticleSerializer


class MyFeedViewSet(viewsets.ReadOnlyModelViewSet):
    """ Feeds endpoint to get a list of feeds a user subcribed to"""

    queryset = Feed.objects.all()
    def get_queryset(self):                                    
        return super().get_queryset().filter(subscribers__id=self.request.user.id)
    serializer_class = FeedSerializer

