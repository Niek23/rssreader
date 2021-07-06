from rest_framework.response import Response 

def subscribe_to_feed(user, feed, subsrcibe=True):
    """(Un)Subscribe a user from/to feed and generate response"""
    
    # Check if the user is already subcribed to the feed
    if subsrcibe:
        if feed.subscribers.filter(pk = user.id).exists():
            return Response({'message':f'You are already subscribed to * {feed} * feed'})

        feed.subscribers.add(user)
        return Response({'message': f'You have successfully subscribed to * {feed} * feed'})
     
    if not subsrcibe:
        if not feed.subscribers.filter(pk = user.id).exists():
            return Response({'message':f'You are not subscribed to * {feed} * feed'})

        feed.subscribers.remove(user)
        return Response({'message': f'You have successfully unsubscribed from * {feed} * feed'})


def mark_article_read(user, article, mark=True):
    """(Un)Mark article as read for a user and generate response"""

    if mark:
        # Check if the article is already marked read
        if article.is_read_by.filter(pk = user.id).exists():
            return Response({'message':f'The article * {article} * is already marked READ'})

        article.is_read_by.add(user)
        return Response({'message': f'You have successfully marked the article * {article} * READ'})
    
    if not mark:
        # Check if the article is not marked read
        if not article.is_read_by.filter(pk = user.id).exists():
            return Response({'message':f'The article * {article} * is already marked UNREAD'})

        article.is_read_by.remove(user)
        return Response({'message': f'You have successfully marked the article * {article} * UNREAD'})
