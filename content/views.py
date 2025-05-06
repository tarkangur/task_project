from .models import Post, Comment
from rest_framework import viewsets
from .serializers import PostSerializer, CommentSerializer


class PostCreate(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostList(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer