from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.core.cache import cache


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        cache_key = f'posts_list_user_{request.user.pk}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        data_cache = response.data
        cache.set(cache_key, data_cache)
        return Response(data_cache)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        cache_key = f'post_{post.pk}_comments_user_{request.user.pk}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        data = serializer.data
        cache.set(cache_key, data)
        return Response(data)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        return Comment.objects.filter(post__user=self.request.user)

    def perform_create(self, serializer):
        post_instance = serializer.validated_data.get('post')
        if post_instance and post_instance.user != self.request.user:
            raise PermissionDenied("You can only create comments on your own posts.")
        serializer.save()

    def list(self, request, *args, **kwargs):
        cache_key = f'comments_list_user_{request.user.pk}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        data_cache = response.data
        cache.set(cache_key, data_cache)
        return Response(data_cache)
