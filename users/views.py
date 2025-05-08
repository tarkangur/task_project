from .models import Users
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer
from content.serializers import PostSerializer
from media.serializers import AlbumSerializer
from todos.serializers import TodoSerializer
from django.core.cache import cache


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'users_list'

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        data_cache = response.data

        cache.set(cache_key, data_cache)

        return response

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        user = self.get_object()
        cache_key = f'user_posts_{user.pk}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        posts = user.posts.all()
        serializer = PostSerializer(posts, many=True)
        data = serializer.data
        cache.set(cache_key, data)

        return Response(data)

    @action(detail=True, methods=['get'])
    def albums(self, request, pk=None):
        user = self.get_object()
        cache_key = f'user_albums_{user.pk}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        albums = user.albums.all()
        serializer = AlbumSerializer(albums, many=True)
        data = serializer.data
        cache.set(cache_key, data)

        return Response(data)

    @action(detail=True, methods=['get'])
    def todos(self, request, pk=None):
        user = self.get_object()
        cache_key = f'user_todos_{user.pk}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        todos = user.todos.all()
        serializer = TodoSerializer(todos, many=True)
        data = serializer.data
        cache.set(cache_key, data)

        return Response(data)
