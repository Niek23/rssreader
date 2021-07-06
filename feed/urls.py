from .views import FeedViewSet, ArticleViewSet, MyFeedViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

feeds_router = DefaultRouter()
myfeeds_router = DefaultRouter()

feeds_router.register(r'feeds', FeedViewSet)
myfeeds_router.register(r'my-feeds', MyFeedViewSet)

feeds_articles_router = routers.NestedSimpleRouter(feeds_router, r'feeds', lookup='feed')
myfeeds_articles_router = routers.NestedSimpleRouter(myfeeds_router, r'my-feeds', lookup='feed')

feeds_articles_router.register(r'articles', ArticleViewSet, basename='feed-article')
myfeeds_articles_router.register(r'articles', ArticleViewSet, basename='myfeed-article')

urlpatterns = [

    # /feeds
    # /feeds/<id>
    path('', include(feeds_router.urls)),

    # /feeds/<id>/articles
    # /feeds/<id>/articles/<id>
    path('', include(feeds_router.urls)),

    # /my-feeds
    # /my-feeds/<id>
    path('', include(myfeeds_router.urls)),

    # /my-feeds/<id>/articles
    # /feeds/<id>/articles/<id>
    path('', include(myfeeds_articles_router.urls)),


] 