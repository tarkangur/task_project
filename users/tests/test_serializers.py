from django.test import TestCase
from django.contrib.auth import get_user_model
from ..serializers import UserSerializer

User = get_user_model()


class UserSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="Test1",
            email="Test1@mail.com",
            password="123456",
            first_name="Test",
            last_name="Model",
            street="sokak",
            suite="gop",
            city="istanbul",
            zipcode=12345,
            phone="5555555555",
            website="https://test1.com",
            company_name="Test1 comp"
        )

        self.user_data = {
            'username': 'Test2',
            'email': 'Test2@mail.com',
            'password': '123456',
            'first_name': 'Test2',
            'last_name': 'Model',
            'street': 'sk',
            'suite': 'suite',
            'city': 'Ankara',
            'zipcode': 34342,
            'phone': '6666666666',
            'website': 'https://test2.com',
            'company_name': 'Test2 comp'
        }

    def test_serializer_serialization(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data

        self.assertEqual(data['id'], self.user.id)
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['phone'], self.user.phone)
        self.assertEqual(data['website'], self.user.website)
        self.assertEqual(data['name'], 'Test Model')

        self.assertIsInstance(data['address'], dict)
        self.assertEqual(data['address']['street'], self.user.street)
        self.assertEqual(data['address']['city'], self.user.city)
        self.assertIn('geo', data['address'])
        self.assertIsInstance(data['address']['geo'], dict)

        self.assertIsInstance(data['company'], dict)
        self.assertEqual(data['company']['name'], self.user.company_name)

    def test_serializer_deserialization_valid_data(self):
        serializer = UserSerializer(data=self.user_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['username'], self.user_data['username'])
        self.assertEqual(serializer.validated_data['email'], self.user_data['email'])
        self.assertEqual(serializer.validated_data['street'], self.user_data['street'])
        self.assertEqual(serializer.validated_data['company_name'], self.user_data['company_name'])

    def test_serializer_create_method(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()

        self.assertIsNotNone(user.pk)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))

    def test_serializer_update_method(self):
        update_data = {
            'email': 'update@mail.com',
            'street': 'Update',
            'password': 'updatepass'
        }

        serializer = UserSerializer(instance=self.user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated_user = serializer.save()

        self.assertEqual(updated_user.email, update_data['email'])
        self.assertEqual(updated_user.street, update_data['street'])
        self.assertTrue(updated_user.check_password(update_data['password']))
        self.assertEqual(updated_user.username, self.user.username)
