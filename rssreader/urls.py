from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="RSS Reader API",
      default_version='v1',
      description="RSS Reader provides the possiblity to subscribe for various feeds,\
                  mark articles and filter them.",
      contact=openapi.Contact(email="nkt.gonchar@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'auth/', include('users.urls')),
    path(r'api/', include('feed.urls')),

    # Documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
