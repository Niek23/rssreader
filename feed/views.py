from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import FeedSerializer, ArticleSerializer
from .services import subscribe_to_feed, mark_article_read, filter_read, get_updating_status
from .models import Feed, Article


class WarningViewSet(viewsets.ReadOnlyModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        feed_pk = self.kwargs.get('feed_pk')
        status = get_updating_status(Feed, feed_pk)
        response = {'auto-update': status,
                    'data': serializer.data}
        return Response(response)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        status = get_updating_status(Feed)
        response = {'auto-update': status,
                    'data': serializer.data}
        return Response(response)


class FeedViewSet(WarningViewSet):
    """Feeds endpoint to get one or all feeds and (un)subscribe to the selected one"""

    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    @action(methods=['POST', 'DELETE'], detail=True, url_path='subscribe')
    def subscribe(self, request, pk=None):
        """Feed endpoint to (un)subscribe the user from/to the feed"""
        if request.method == 'POST':
            return subscribe_to_feed(request.user, self.get_object())
        if request.method == 'DELETE':
            return subscribe_to_feed(request.user, self.get_object(), subscribe=False)

    @action(methods=['POST'], detail=True, url_path='force-update')
    def force_update(self, request, pk=None):
        """Feed endpoint to load new articles"""
        new_articles = Feed.objects.update_feed_content(self.get_object())
        return Response({'new_entries': ArticleSerializer(new_articles, many=True).data})

    @action(methods=['POST'], detail=True, url_path='retry-updates')
    def retry_updates(self, request, pk=None):
        feed = self.get_object()
        feed.updating = True
        feed.save()
        return Response({'auto-update': 'restarting', 'feed': FeedSerializer(feed).data})


class MyFeedViewSet(WarningViewSet):
    """ Feeds endpoint to get a list of feeds a user subcribed to"""

    queryset = Feed.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(subscribers__id=self.request.user.id)
    serializer_class = FeedSerializer


class ArticleViewSet(WarningViewSet):
    """ Article endpoint to get one or all artcles for the selected feed"""

    queryset = Article.objects.all().order_by('-created')
    serializer_class = ArticleSerializer

    def get_queryset(self):
        # Filter per feed and read/unread based on read paramenter in url
        read = self.request.query_params.get(
            'read')  # URLparam - read=True/False
        feed_pk = self.kwargs.get('feed_pk')
        qs = super().get_queryset()
        if feed_pk:
            qs = qs.filter(feed=self.kwargs['feed_pk'])
        return filter_read(qs, read, self.request)

    @action(methods=['POST', 'DELETE'], detail=True, url_path='mark-read')
    def mark_read(self, request, pk=None, feed_pk=None):
        """Endpoint to (un)mark an article as read"""
        user = request.user
        article = self.get_object()
        if request.method == 'POST':
            return mark_article_read(user, article)
        if request.method == 'DELETE':
            return mark_article_read(user, article, is_read=False)
