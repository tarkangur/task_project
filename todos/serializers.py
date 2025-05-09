from rest_framework import serializers
from .models import Todo
from django.contrib.auth import get_user_model

User = get_user_model()


class TodoSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(source='user', read_only=True)

    class Meta:
        model = Todo
        fields = ['userId', 'id', 'title', 'completed', 'user']

        extra_kwargs = {
            'user': {'write_only': True},
        }
