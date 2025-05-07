from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(source='user', read_only=True)

    class Meta:
        model = Todo
        fields = ['userId', 'id', 'title', 'completed']
