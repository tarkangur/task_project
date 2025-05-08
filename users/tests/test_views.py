from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from content.models import Post
from media.models import Album
from todos.models import Todo

User = get_user_model()


class UserAPITest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='Test1', email='Test1@mail.com', password='123456')
        self.user2 = User.objects.create_user(username='Test2', email='Test2@mail.com', password='654321')

        self.client.force_authenticate(user=self.user1)

        self.list_url = reverse('users-list')
        self.detail_url = reverse('users-detail', kwargs={'pk': self.user1.pk})

        self.post1 = Post.objects.create(user=self.user1, title='Test1 Post 1', body='Testing1')
        self.post2 = Post.objects.create(user=self.user1, title='Test1 Post 2', body='Testing2')
        self.album1 = Album.objects.create(user=self.user1, title='Test1 Album 1')
        self.todo1 = Todo.objects.create(user=self.user1, title='Test1 Todo 1', completed=False)

        self.user_posts_url = reverse('users-posts', kwargs={'pk': self.user1.pk})
        self.user_albums_url = reverse('users-albums', kwargs={'pk': self.user1.pk})
        self.user_todos_url = reverse('users-todos', kwargs={'pk': self.user1.pk})

    def test_list_users(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        new_user_data = {
            'username': 'Test3',
            'email': 'Test3@mail.com',
            'password': '987654',
            'first_name': 'Test3',
            'last_name': 'Model',
            'street': 'sk', 'suite': 'konak', 'city': 'izmir', 'zipcode': 98765,
            'phone': '9999999999', 'website': 'https://Test3.com', 'company_name': 'Test3 comp'
        }

        response = self.client.post(self.list_url, data=new_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), 3)
        new_user = User.objects.get(username='Test3')
        self.assertEqual(new_user.email, new_user_data['email'])
        self.assertTrue(new_user.check_password(new_user_data['password']))

    def test_create_user_with_missing_data(self):
        invalid_data = {'username': 'uName'}

        response = self.client.post(self.list_url, data=invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertIn('password', response.data)

    def test_retrieve_user(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['username'], self.user1.username)
        self.assertEqual(response.data['email'], self.user1.email)

    def test_update_user(self):
        update_data = {
            'username': 'updateduser1',
            'email': 'updated@example.com',
            'password': 'newpassw',
            'first_name': 'Updated',
            'last_name': 'User',
            'street': 'Upd St', 'suite': 'Upd Sui', 'city': 'Upd City', 'zipcode': 55555,
            'phone': '2222222222', 'website': 'https://upd.com', 'company_name': 'Upd Comp'
        }

        response = self.client.put(self.detail_url, data=update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.email, update_data['email'])
        self.assertTrue(self.user1.check_password(update_data['password']))

    def test_delete_user(self):
        user_to_delete_pk = self.user2.pk
        delete_url = reverse('users-detail', kwargs={'pk': user_to_delete_pk})

        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(User.objects.count(), 1)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=user_to_delete_pk)

    def test_user_posts_action(self):
        response = self.client.get(self.user_posts_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), self.user1.posts.count())

        if response.data:
            self.assertEqual(response.data[0]['userId'], self.user1.pk)

    def test_user_albums_action(self):
        response = self.client.get(self.user_albums_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_user_todos_action(self):
        response = self.client.get(self.user_todos_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
