from rest_framework import serializers
from .models import Album, Photo
from django.contrib.auth import get_user_model

User = get_user_model()


class AlbumSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(source='user', read_only=True)

    class Meta:
        model = Album
        fields = ['userId', 'id', 'title', 'user']

        extra_kwargs = {
            'user': {'write_only': True, 'required': False},
        }


class PhotoSerializer(serializers.ModelSerializer):
    albumId = serializers.PrimaryKeyRelatedField(source='album', read_only=True)

    class Meta:
        model = Photo
        fields = ['albumId', 'id', 'title', 'url', 'thumbnailUrl', 'album']

        extra_kwargs = {
            'album': {'write_only': True},
        }
