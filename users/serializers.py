from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

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
        fields = ['id', 'username', 'email', 'phone', 'website', 'name','address',  'company', 'password', 'first_name',
                  'last_name', 'street', 'suite', 'city', 'zipcode', 'company_name', 'lat', 'lng']
        read_only_fields = ('id',)

        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'street': {'write_only': True},
            'suite': {'write_only': True},
            'city': {'write_only': True},
            'zipcode': {'write_only': True},
            'company_name': {'write_only': True},
            'lat': {'write_only': True},
            'lng': {'write_only': True},
        }

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        extra_fields = validated_data

        user = Users.objects.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
