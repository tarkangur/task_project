from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
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
            website="www.test1.com",
            company_name="Test1 comp"
        )

    def test_str(self):
        self.assertEqual(str(self.user), "Test1")

    def test_user_values(self):
        self.assertEqual(self.user.username, "Test1")
        self.assertEqual(self.user.email, "Test1@mail.com")
        self.assertTrue(self.user.check_password("123456"))
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "Model")
        self.assertEqual(self.user.street, "sokak")
        self.assertEqual(self.user.suite, "gop")
        self.assertEqual(self.user.city, "istanbul")
        self.assertEqual(self.user.zipcode, 12345)
        self.assertEqual(self.user.phone, "5555555555")
        self.assertEqual(self.user.website, "www.test1.com")
        self.assertEqual(self.user.company_name, "Test1 comp")

    def test_user_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), "Test Model")
