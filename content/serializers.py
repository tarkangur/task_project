from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(source='user', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'userId', 'title', 'body', 'user']
        extra_kwargs = {
            'user': {'write_only': True, 'required': True},
        }


class CommentSerializer(serializers.ModelSerializer):
    postId = serializers.PrimaryKeyRelatedField(source='post', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'postId', 'name', 'email', 'body', 'post']

        extra_kwargs = {
            'post': {'write_only': True, 'required': True},
        }
