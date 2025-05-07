from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    def get_name(self, obj: Users):
        full_name = f"{obj.first_name} {obj.last_name}".strip()
        return full_name

    def get_address(self, obj: Users):
        address_data = {
            'street': obj.street,
            'suite': obj.suite,
            'city': obj.city,
            'zipcode': obj.zipcode,
            'geo': {
                'lat': obj.lat,
                'lng': obj.lng
            }
        }
        return address_data

    def get_company(self, obj: Users):

        company_data = {
            'name': obj.company_name,
        }
        return company_data

    class Meta:
        model = Users
        fields = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']
