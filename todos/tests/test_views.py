from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Todo
from django.contrib.auth import get_user_model

User = get_user_model()


class TodoAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='TestTodo1', email='Test1@example.com', password='123456')

        self.client.force_authenticate(user=self.user)

        self.todo1 = Todo.objects.create(user=self.user, title='Test Todo 1', completed=False)
        self.todo2 = Todo.objects.create(user=self.user, title='Test Todo 2', completed=True)

        self.other_user = User.objects.create_user(username='user_todo', email='user@example.com', password='11111')
        self.other_todo = Todo.objects.create(user=self.other_user, title='Other User Todo', completed=False)

        self.list_url = reverse('todo-list')
        self.detail_url = reverse('todo-detail', kwargs={'pk': self.todo1.pk})
        self.other_detail_url = reverse('todo-detail', kwargs={'pk': self.other_todo.pk})

    def test_list_todos(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), Todo.objects.filter(user=self.user).count())
        for todo_data in response.data:
             self.assertEqual(todo_data['userId'], self.user.pk)

    def test_list_todos_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_todo(self):
        new_todo_data = {
            'user': self.user.pk,
            'title': 'New Test Todo from API',
            'completed': False,
        }

        response = self.client.post(self.list_url, data=new_todo_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Todo.objects.count(), 4)

        new_todo = Todo.objects.get(title='New Test Todo from API')
        self.assertEqual(new_todo.user, self.user)
        self.assertEqual(new_todo.completed, False)

    def test_create_todo_unauthenticated(self):
        self.client.force_authenticate(user=None)
        new_todo_data = {'title': 'Unauthorized Todo', 'completed': False}
        response = self.client.post(self.list_url, data=new_todo_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_todo(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], self.todo1.pk)
        self.assertEqual(response.data['title'], self.todo1.title)
        self.assertEqual(response.data['completed'], self.todo1.completed)
        self.assertEqual(response.data['userId'], self.user.pk)

    def test_retrieve_other_users_todo(self):
        response = self.client.get(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_todo(self):
        update_data = {
            'user': self.user.pk,
            'title': 'Updated Test Todo via API',
            'completed': True,
        }

        response = self.client.put(self.detail_url, data=update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, update_data['title'])
        self.assertEqual(self.todo1.completed, update_data['completed'])
        self.assertEqual(self.todo1.user, self.user)

    def test_update_other_users_todo(self):
        update_data = {'title': 'Attempted Update', 'completed': True}
        response = self.client.put(self.other_detail_url, data=update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.other_todo.refresh_from_db()
        self.assertNotEqual(self.other_todo.title, update_data['title'])

    def test_delete_todo(self):
        todo_to_delete_pk = self.todo2.pk
        delete_url = reverse('todo-detail', kwargs={'pk': todo_to_delete_pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Todo.objects.count(), 2)

        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(pk=todo_to_delete_pk)

    def test_delete_other_users_todo(self):
        response = self.client.delete(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Todo.objects.count(), 3)
        self.assertTrue(Todo.objects.filter(pk=self.other_todo.pk).exists())
