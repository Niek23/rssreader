import pytest
from task_scheduler.tasks import update_feeds
from feed.models import Feed


class TestUpdateFeeds:
    
    @pytest.mark.django_db(transaction=True)
    def test_update_feed(self, empty_feed, broker, worker):
        assert empty_feed.article_set.all().count() == 0, \
            'The testing feed is not empty'
        
        update_feeds.send()

        broker.join('default')
        worker.join()
        assert empty_feed.article_set.all().count() > 0, \
            'Check the tasks, the articles are not updating'
        
        assert Feed.objects.all().first().updating, \
            'Feed updating flag toggled to false after succesfull update'
    
    
    @pytest.mark.django_db(transaction=True)
    def test_update_feed_error(self, empty_feed, broker, worker):
        
        empty_feed.link = 'broken link'
        empty_feed.save()
        update_feeds.send()
        
        
        broker.join('default')
        worker.join()
        
        assert not Feed.objects.all().first().updating, \
            'Failing tasks does not toggle feed updating to False'

    @pytest.mark.django_db(transaction=True)
    def test_update_feed_error_user_retry(self, empty_feed, broker, worker, user_client):
        
        empty_feed.updating = False
        empty_feed.save()
        response = user_client.get(f'/api/feeds/')
        assert response.json().get('auto-update') == '1 feed is not updating'
        update_feeds.send()
        broker.join('default')
        worker.join()
        assert not Feed.objects.all().first().updating, \
            'The False status should not be toggled after task execution'
        
        user_client.get(f'/api/feeds/{empty_feed.id}/retry-updates/')
        
        assert Feed.objects.all().first().updating, \
            '/retry-update/ does not make updating True for the requested feed'

        update_feeds.send()
        broker.join('default')
        worker.join()
        assert empty_feed.article_set.all().count() > 0, \
            'The feed is not updating after user restarted'

        response = user_client.get(f'/api/feeds/')
        assert response.json().get('auto-update') == 'All feeds are updating every minute'
