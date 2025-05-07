from rest_framework import serializers
from .models import Users, Address, Company


class GeoSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(source='geo_lat')
    lng = serializers.FloatField(decimal_places=6, source='geo_lng')


class AddressSerializer(serializers.ModelSerializer):

    geo = GeoSerializer()

    class Meta:
        model = Address
        fields = ['street', 'suite', 'city', 'zipcode', 'geo']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    model = Users
    fields = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']