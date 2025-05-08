from .models import Post, Comment
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer
from django.core.cache import cache


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'Posts_list'

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        data_cache = response.data

        cache.set(cache_key, data_cache)

        return response

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        cache_key = f'post_comments_{post.pk}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        comment = post.comments.all()
        serializer = CommentSerializer(comment, many=True)
        data = serializer.data
        cache.set(cache_key, data)

        return Response(data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'Comments_list'

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        data_cache = response.data

        cache.set(cache_key, data_cache)

        return response
