from django.test import TestCase
from django.contrib.auth import get_user_model
from ..serializers import TodoSerializer
from ..models import Todo

User = get_user_model()


class TodoSerializersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="Todo Test1", email="todoTest1@mail.com", password="123456")

        self.todo_instance = Todo.objects.create(
            user=self.user,
            title='Title',
            completed=False
        )

        self.valid_todo_data = {
            'user': self.user.pk,
            'title': 'New Todo',
            'completed': True
        }

        self.invalid_todo_data = {
            'completed': True
        }

        self.update_todo_data = {
            'title': 'Updated Todo Title',
            'completed': True
        }

    def test_serializers_serialization(self):
        serializer = TodoSerializer(instance=self.todo_instance)
        data = serializer.data

        self.assertEqual(data['id'], self.todo_instance.id)
        self.assertEqual(data['title'], self.todo_instance.title)
        self.assertEqual(data['completed'], self.todo_instance.completed)
        self.assertEqual(data['userId'], self.user.pk)

    def test_serializer_deserialization_valid_data(self):
        serializer = TodoSerializer(data=self.valid_todo_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['user'], self.user)
        self.assertEqual(serializer.validated_data['title'], self.valid_todo_data['title'])
        self.assertEqual(serializer.validated_data['completed'], self.valid_todo_data['completed'])

    def test_serializer_deserialization_invalid_data(self):
        serializer = TodoSerializer(data=self.invalid_todo_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('user', serializer.errors)

    def test_serializer_create_method(self):
        serializer = TodoSerializer(data=self.valid_todo_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        todo = serializer.save()
        self.assertIsNotNone(todo.pk)
        self.assertEqual(todo.user, self.user)
        self.assertEqual(todo.title, self.valid_todo_data['title'])
        self.assertEqual(todo.completed, self.valid_todo_data['completed'])

    def test_serializer_update_method(self):
        serializer = TodoSerializer(instance=self.todo_instance, data=self.update_todo_data, partial=True)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated_todo = serializer.save()

        self.assertEqual(updated_todo.title, self.update_todo_data['title'])
        self.assertEqual(updated_todo.completed, self.update_todo_data['completed'])
        self.assertEqual(updated_todo.user, self.user)
