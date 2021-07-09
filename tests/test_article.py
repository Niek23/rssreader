import pytest


class TestArticleAPI:

    @pytest.mark.django_db(transaction=True)
    def test_articles_not_found(self, user_client):
        response = user_client.get(f'/api/articles/')
        assert response.status_code != 404, \
            'Route `api/articles/` is not found, check it in *urls.py*'


    @pytest.mark.django_db(transaction=True)
    def test_feed_articles_not_found(self, user_client, another_feed):
        response = user_client.get(f'/api/feeds/{another_feed.id}/articles/')
        assert response.status_code != 404, \
            'Route `api/feeds/<feed_pk>/articles/` is not found, check it in *urls.py*'


    @pytest.mark.django_db(transaction=True)
    def test_myfeed_articles_not_found(self, user_client, feed):
        response = user_client.get(f'/api/my-feeds/{feed.id}/articles/')
        assert response.status_code != 404, \
            'Route `api/<my-feed_pk>/articles/` is not found, check it in *urls.py*'


    @pytest.mark.django_db(transaction=True)
    def test_feed_article_not_found(self, user_client, feed, article):
        response = user_client.get(f'/api/feeds/{feed.id}/articles/{article.id}/')
        assert response.status_code != 404, \
            'Route `api/<feed_pk>/articles/<article_pk>/` is not found, check it in *urls.py*'


    @pytest.mark.django_db(transaction=True)
    def test_myfeed_article_not_found(self, user_client, feed, article):
        response = user_client.get(f'/api/my-feeds/{feed.id}/articles/{article.id}/')
        assert response.status_code != 404, \
            'Route `api/<my-feed_pk>/articles/<article_pk>/` is not found, check it in *urls.py*'


    @pytest.mark.django_db(transaction=True)
    def test_myfeed_article_read(self, user_client, feed, user):
        
        feed.article_set.all().first().is_read_by.set([user]) #mark one article read

        response = user_client.get(f'/api/my-feeds/{feed.id}/articles/?read=False')
        assert len(response.json().get('data')) + 1 == feed.article_set.all().count(), \
            'Route `/api/my-feeds/{feed.id}/articles/?read=False` does not filter unread articles' 

        response = user_client.get(f'/api/my-feeds/{feed.id}/articles/?read=True')
        assert len(response.json().get('data')) == 1, \
            'Route `/api/my-feeds/{feed.id}/articles/?read=True/` does not filter unread articles'


    @pytest.mark.django_db(transaction=True)
    def test_feed_article_read(self, user_client, feed, user):
        
        feed.article_set.all().first().is_read_by.set([user]) #mark one article read

        response = user_client.get(f'/api/feeds/{feed.id}/articles/?read=False')
        assert len(response.json().get('data')) + 1 == feed.article_set.all().count(), \
            'Route `/api/feeds/{feed.id}/articles/?read=False` does not filter unread articles' 

        response = user_client.get(f'/api/feeds/{feed.id}/articles/?read=True')
        assert len(response.json().get('data')) == 1, \
            'Route `/api/feeds/{feed.id}/articles/?read=True/` does not filter unread articles'


    @pytest.mark.django_db(transaction=True)
    def test_feed_articles_mark_read(self, user_client, feed, article):

        # Try mark already read article
        count_before = len(user_client.get(f'/api/feeds/{feed.id}/articles/?read=True').json().get('data'))
        response = user_client.get(f'/api/feeds/{feed.id}/articles/{article.id}/mark-read/')
        assert response.json().get('message') == \
            f'The article * {article.title} * is already marked READ'
        count_after = len(user_client.get(f'/api/feeds/{feed.id}/articles/?read=True').json().get('data'))
        assert count_before == count_after


        # Try unmark one article
        count_before = count_after
        response = user_client.get(f'/api/feeds/{feed.id}/articles/{article.id}/unmark-read/')
        assert response.json().get('message') == \
            f'You have marked the article * {article.title} * UNREAD'
        count_after = len(user_client.get(f'/api/feeds/{feed.id}/articles/?read=True').json().get('data'))
        assert count_before == count_after + 1


        # Try unmark not read article
        count_before = count_after
        response = user_client.get(f'/api/feeds/{feed.id}/articles/{article.id}/unmark-read/')
        assert response.json().get('message') == \
            f'The article * {article.title} * is already marked UNREAD'
        count_after = len(user_client.get(f'/api/feeds/{feed.id}/articles/?read=True').json().get('data'))
        assert count_before == count_after


        # Try mark article read
        count_before = count_after
        response = user_client.get(f'/api/feeds/{feed.id}/articles/{article.id}/mark-read/')
        assert response.json().get('message') == \
            f'You have marked the article * {article.title} * READ'
        count_after = len(user_client.get(f'/api/feeds/{feed.id}/articles/?read=True').json().get('data'))
        assert count_before + 1 == count_after


    @pytest.mark.django_db(transaction=True)
    def test_myfeed_articles_mark_read(self, user_client, feed, article):

        # Try mark already read article
        count_before = len(user_client.get(f'/api/my-feeds/{feed.id}/articles/?read=True').json().get('data'))
        response = user_client.get(f'/api/my-feeds/{feed.id}/articles/{article.id}/mark-read/')
        assert response.json().get('message') == \
            f'The article * {article.title} * is already marked READ'
        count_after = len(user_client.get(f'/api/my-feeds/{feed.id}/articles/?read=True').json().get('data'))
        assert count_before == count_after


        # Try unmark one article
        count_before = count_after
        response = user_client.get(f'/api/my-feeds/{feed.id}/articles/{article.id}/unmark-read/')
        assert response.json().get('message') == \
            f'You have marked the article * {article.title} * UNREAD'
        count_after = len(user_client.get(f'/api/my-feeds/{feed.id}/articles/?read=True').json().get('data'))
        assert count_before == count_after + 1


        # Try unmark not read article
        count_before = count_after
        response = user_client.get(f'/api/my-feeds/{feed.id}/articles/{article.id}/unmark-read/')
        assert response.json().get('message') == \
            f'The article * {article.title} * is already marked UNREAD'
        count_after = len(user_client.get(f'/api/my-feeds/{feed.id}/articles/?read=True').json().get('data'))
        assert count_before == count_after


        # Try mark article read
        count_before = count_after
        response = user_client.get(f'/api/my-feeds/{feed.id}/articles/{article.id}/mark-read/')
        assert response.json().get('message') == \
            f'You have marked the article * {article.title} * READ'
        count_after = len(user_client.get(f'/api/my-feeds/{feed.id}/articles/?read=True').json().get('data'))
        assert count_before + 1 == count_after