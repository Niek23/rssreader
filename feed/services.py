from rest_framework.response import Response
import feedparser
from django.shortcuts import get_object_or_404


def subscribe_to_feed(user, feed, subsrcibe=True):
    """(Un)Subscribe a user from/to feed and generate response"""

    # Check if the user is already subcribed to the feed
    if subsrcibe:
        if feed.subscribers.filter(pk=user.id).exists():
            return Response({'message': f'You are already subscribed to * {feed} * feed'})

        feed.subscribers.add(user)
        return Response({'message': f'You have successfully subscribed to * {feed} * feed'})

    if not subsrcibe:
        if not feed.subscribers.filter(pk=user.id).exists():
            return Response({'message': f'You are not subscribed to * {feed} * feed'})

        feed.subscribers.remove(user)
        return Response({'message': f'You have successfully unsubscribed from * {feed} * feed'})


def mark_article_read(user, article, is_read=True):
    """(Un)Mark article as read for a user and generate response"""

    if is_read:
        # Check if the article is already marked read
        if article.is_read_by.filter(pk=user.id).exists():
            return Response({'message': f'The article * {article} * is already marked READ'})

        article.is_read_by.add(user)
        return Response({'message': f'You have marked the article * {article} * READ'})

    if not is_read:
        # Check if the article is not marked read
        if not article.is_read_by.filter(pk=user.id).exists():
            return Response({'message': f'The article * {article} * is already marked UNREAD'})

        article.is_read_by.remove(user)
        return Response({'message': f'You have marked the article * {article} * UNREAD'})


def filter_read(query_set, read, request):
    """Check if read=(true/false) paramter is in url, filter and return queryset"""

    if read is not None:
        if read == 'True':
            return query_set.filter(is_read_by__id=request.user.id)
        if read == 'False':
            return query_set.exclude(is_read_by__id=request.user.id)
    return query_set


def get_valid_feed(link):
    """Check is the provided feed is a valid and return it"""

    feed = feedparser.parse(link)
    if feed['bozo'] == 1:
        raise feed['bozo_exception']
    return feed


def get_updating_status(Feed, feed_pk=None):
    """Return updating status based on the number of udpating feeds"""

    if feed_pk:
        status = get_object_or_404(Feed, pk=feed_pk).updating
    else:
        not_updating = Feed.objects.filter(updating=False).count()
        if not not_updating:
            status = 'All feeds are updating every minute'
        else:
            if not_updating == 1:
                status = '1 feed is not updating'
            else:
                status = f'{not_updating} feeds are not updating'
    return status
