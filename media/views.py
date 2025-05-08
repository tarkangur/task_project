from .models import Album, Photo
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import AlbumSerializer, PhotoSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    @action(detail=True, methods=['get'])
    def photos(self, request, pk=None):
        user = self.get_object()
        photos = user.photos.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
