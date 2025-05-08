from .models import Album, Photo
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import AlbumSerializer, PhotoSerializer
from django.core.cache import cache


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'Albums_list'

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
        cache_key = f'album_photos_{album.pk}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        photos = album.photos.all()
        serializer = PhotoSerializer(photos, many=True)
        data = serializer.data
        cache.set(cache_key, data)

        return Response(data)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'Photos_list'

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        data_cache = response.data

        cache.set(cache_key, data_cache)

        return response
