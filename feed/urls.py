from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from .views import FeedViewSet, ArticleViewSet, MyFeedViewSet

router = SimpleRouter()

router.register(r'feeds', FeedViewSet, basename='feeds')
router.register(r'my-feeds', MyFeedViewSet, basename='my-feeds')
router.register(r'articles', ArticleViewSet, basename='articles')

feeds_articles_router = routers.NestedSimpleRouter(
    router, r'feeds', lookup='feed')
myfeeds_articles_router = routers.NestedSimpleRouter(
    router, r'my-feeds', lookup='feed')

feeds_articles_router.register(
    r'articles', ArticleViewSet, basename='feed-article')
myfeeds_articles_router.register(
    r'articles', ArticleViewSet, basename='myfeed-article')

urlpatterns = [

    # /feeds/<id>/articles
    # /feeds/<id>/articles/<id>
    path('', include(feeds_articles_router.urls)),

    # /my-feeds/<id>/articles
    # /my-feeds/<id>/articles/<id>
    path('', include(myfeeds_articles_router.urls)),

    # /feeds
    # /feeds/<id>
    # /my-feeds
    # /my-feeds/<id>
    # /articles
    # /articles/<id>
    path('', include(router.urls))


]
