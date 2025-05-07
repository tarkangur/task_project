from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(source='user', read_only=True)

    class Meta:
        model = Post
        fields = ['userId', 'id', 'title', 'body']


class CommentSerializer(serializers.ModelSerializer):
    postId = serializers.PrimaryKeyRelatedField(source='post', read_only=True)

    class Meta:
        model = Comment
        fields = ['postId', 'id', 'name', 'email', 'body']
