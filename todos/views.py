from .models import Todo
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import TodoSerializer
from django.core.cache import cache


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'Todos_list'

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        data_cache = response.data

        cache.set(cache_key, data_cache)

        return response
