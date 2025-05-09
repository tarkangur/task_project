from django.test import TestCase
from ..models import Todo
from django.contrib.auth import get_user_model

User = get_user_model()


class TodoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="TodoTest", email="TodoTest@mail.com", password="123456")

        self.todo = Todo.objects.create(user=self.user, title="Test Todo1", completed=False)

    def test_todo_creation(self):
        self.assertIsNotNone(self.todo.pk)
        self.assertEqual(self.todo.user, self.user)
        self.assertEqual(self.todo.title, "Test Todo1")
        self.assertFalse(self.todo.completed)

    def test_todo_completed_default(self):
        new_todo = Todo.objects.create(user=self.user, title="Test2")
        self.assertFalse(new_todo.completed)

    def test_todo_user(self):
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError):
            Todo.objects.create(
                user=None,
                title='User Test',
                completed=False
            )
