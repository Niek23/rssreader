import pytest
from feed.models import Feed


class TestFeedAPI:

    @pytest.mark.django_db(transaction=True)
    def test_feeds_not_found(self, user_client):
        response = user_client.get(f'/api/feeds/')
        assert response.status_code != 404, \
            'Route `api/feeds/` is not found, check it in *urls.py*'


    @pytest.mark.django_db(transaction=True)
    def test_myfeeds_not_found(self, user_client):
        response = user_client.get(f'/api/my-feeds/')
        assert response.status_code != 404, \
            'Route `api/my-feeds/` is not found, check it in *urls.py*'


    @pytest.mark.django_db(transaction=True)
    def test_feed_not_found(self, user_client, feed):
        response = user_client.get(f'/api/feeds/{feed.id}/')
        assert response.status_code != 404, \
            'Route `api/feeds/<feed_pk>/` is not found, check it in *urls.py*'


    @pytest.mark.django_db(transaction=True)
    def test_myfeed_not_found(self, user_client, feed):
        response = user_client.get(f'/api/my-feeds/{feed.id}/')
        assert response.status_code != 404, \
            'Route `api/my-feeds/<feed_pk>/` is not found, check it in *urls.py*'


    @pytest.mark.django_db(transaction=True)
    def test_feeds_subscribe(self, user_client, feed):

        assert feed.subscribers.all().count() == 1, \
            f'Check fixture data. There should be 1 subscriber for {feed.title}'

        response = user_client.get(f'/api/feeds/{feed.id}/subscribe/')
        assert response.json().get('message') == \
            f'You are already subscribed to * {feed.title} * feed'
        
        assert feed.subscribers.all().count() == 1, \
            f'Route /api/feeds/<feed_id>/subscribe/ unsubscribed user from the feed'
        
        response = user_client.get(f'/api/feeds/{feed.id}/unsubscribe/')
        assert response.json().get('message') == \
            f'You have successfully unsubscribed from * {feed.title} * feed'
        
        assert feed.subscribers.all().count() == 0, \
            f'Route /api/feeds/<feed_id>/unsubscribe/ does not work'

        response = user_client.get(f'/api/feeds/{feed.id}/unsubscribe/')
        assert response.json().get('message') == \
            f'You are not subscribed to * {feed.title} * feed'
        
        assert feed.subscribers.all().count() == 0, \
            f'Route /api/feeds/<feed_id>/unsubscribe/ subscribed user for the feed'
    

    @pytest.mark.django_db(transaction=True)
    def test_update_articles(self, user_client, feed):
        response = user_client.get(f'/api/feeds/{feed.id}/force-update/')
        assert 'new_entries' in response.json(), \
            'Make sure `/api/feeds/<feed.id>/update-articles/` updates articles and returns them'


    @pytest.mark.django_db(transaction=True)
    def test_create_feed_method(self):
        feed = Feed.objects.create_feed('https://feeds.feedburner.com/tweakers/mixed')
        assert feed.article_set.all().count() > 0


    @pytest.mark.django_db(transaction=True)
    def test_update_feed_content(self):
        feed = Feed.objects.create_feed('https://feeds.feedburner.com/tweakers/mixed')
        feed.article_set.all().delete()
        assert feed.article_set.all().count() == 0
        Feed.objects.update_feed_content(feed)
        assert feed.article_set.all().count() > 0
