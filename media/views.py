from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Album, Photo
from .serializers import AlbumSerializer, PhotoSerializer
from django.core.cache import cache
from rest_framework.exceptions import PermissionDenied


class AlbumViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AlbumSerializer

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        cache_key = f'album_list_user_{request.user.pk}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        data_cache = response.data
        cache.set(cache_key, data_cache)
        return response

    @action(detail=True, methods=['get'])
    def photos(self, request, pk=None):
        album = self.get_object()
        cache_key = f'album_{album.pk}_photos'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        photos = album.photos.all()
        serializer = PhotoSerializer(photos, many=True)
        data = serializer.data
        cache.set(cache_key, data)

        return Response(data)


class PhotoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(album__user=self.request.user)

    def perform_create(self, serializer):
        album = serializer.validated_data.get('album')

        if album is None or album.user != self.request.user:
            raise PermissionDenied("You can only create photos in your own albums.")

        serializer.save()

    def list(self, request, *args, **kwargs):
        cache_key = f'photo_list_user_{request.user.pk}'

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        data_cache = response.data

        cache.set(cache_key, data_cache)

        return response
