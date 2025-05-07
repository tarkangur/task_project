from rest_framework import serializers
from .models import Album, Photo


class AlbumSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(source='user', read_only=True)

    class Meta:
        model = Album
        fields = ['userId', 'id', 'title']


class PhotoSerializer(serializers.ModelSerializer):
    albumId = serializers.PrimaryKeyRelatedField(source='album', read_only=True)

    class Meta:
        model = Photo
        fields = ['albumId', 'id', 'title', 'url', 'thumbnailUrl']
