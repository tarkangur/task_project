from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import UserViewSet
from todos.views import TodoViewSet
from content.views import PostViewSet, CommentViewSet
from media.views import AlbumViewSet, PhotoViewSet


router = routers.DefaultRouter()


router.register(r'users', UserViewSet, basename='user')
router.register(r'todos', TodoViewSet, basename='todo')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'photos', PhotoViewSet, basename='photo')


schema_view = get_schema_view(
   openapi.Info(
      title="Proje API Dokümantasyonu",
      default_version='v1',
      description="Bu API, kullanıcı, todo, içerik ve medya yönetimi için endpointler sunar.",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('v1/', include(router.urls)),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
