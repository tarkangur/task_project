from rest_framework import serializers
from .models import Users


class GeoSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(source='geo_lat')
    lng = serializers.FloatField(decimal_places=6, source='geo_lng')


class UserSerializer(serializers.ModelSerializer):
    model = Users
    fields = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']