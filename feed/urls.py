from .views import FeedViewSet, ArticleViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'feeds', FeedViewSet)
feeds_router = routers.NestedSimpleRouter(router, r'feeds', lookup='feed')
feeds_router.register(r'articles', ArticleViewSet, basename='feed-article')


urlpatterns = [

    # /feeds
    # /feeds/<id>
    path('', include(router.urls)),

    # /feeds/<id>/articles
    # /feeds/<id>/articles/<id>
    path('', include(feeds_router.urls))

] 