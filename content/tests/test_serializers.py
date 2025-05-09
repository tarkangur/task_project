from django.test import TestCase
from ..serializers import CommentSerializer, PostSerializer
from ..models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser_post_serializer', email='postserializer@example.com', password='password123')

        self.post_instance = Post.objects.create(
            user=self.user,
            title='Existing Post for Serialization',
            body='Body of existing post.'
        )

        self.valid_post_data = {
            'user': self.user.pk,
            'title': 'New Post from Test Data',
            'body': 'Body of new post.'
        }

        self.invalid_post_data = {
            'title': 'Post without User and Body',
        }

        self.update_post_data = {
            'title': 'Updated Post Title',
            'body': 'Updated body of post.'
        }

    def test_post_serializer_serialization(self):
        serializer = PostSerializer(instance=self.post_instance)
        data = serializer.data

        self.assertEqual(data['id'], self.post_instance.id)
        self.assertEqual(data['title'], self.post_instance.title)
        self.assertEqual(data['body'], self.post_instance.body)
        self.assertEqual(data['userId'], self.user.pk)
        self.assertNotIn('user', data)

    def test_post_serializer_deserialization_valid_data(self):
        serializer = PostSerializer(data=self.valid_post_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertEqual(serializer.validated_data['user'], self.user)
        self.assertEqual(serializer.validated_data['title'], self.valid_post_data['title'])
        self.assertEqual(serializer.validated_data['body'], self.valid_post_data['body'])

        self.assertNotIn('userId', serializer.validated_data)

    def test_post_serializer_deserialization_invalid_data(self):
        serializer = PostSerializer(data=self.invalid_post_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('user', serializer.errors)
        self.assertIn('body', serializer.errors)
        self.assertNotIn('userId', serializer.errors)

    def test_post_serializer_create_method(self):
        serializer = PostSerializer(data=self.valid_post_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        post = serializer.save()

        self.assertIsNotNone(post.pk)
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.title, self.valid_post_data['title'])
        self.assertEqual(post.body, self.valid_post_data['body'])

    def test_post_serializer_update_method(self):
        serializer = PostSerializer(instance=self.post_instance, data=self.update_post_data, partial=True)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated_post = serializer.save()

        self.post_instance.refresh_from_db()
        self.assertEqual(self.post_instance.title, self.update_post_data['title'])
        self.assertEqual(self.post_instance.body, self.update_post_data['body'])
        self.assertEqual(self.post_instance.user, self.user)


class CommentSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser_comment_serializer', email='commentserializer@example.com', password='password123')
        self.post = Post.objects.create(user=self.user, title='Comment Test Post', body='Body for comment test.')

        self.comment_instance = Comment.objects.create(
            post=self.post,
            name='Existing Comment User',
            email='existing@example.com',
            body='Body of existing comment.'
        )

        self.valid_comment_data = {
            'post': self.post.pk,
            'name': 'New Comment User',
            'email': 'new@example.com',
            'body': 'Body of new comment.'
        }
        self.invalid_comment_data = {
            'name': 'Incomplete Comment',
            'body': 'This comment is missing post and email.'
        }

        self.update_comment_data = {
            'body': 'Updated body of comment.'
        }

    def test_comment_serializer_serialization(self):
        serializer = CommentSerializer(instance=self.comment_instance)
        data = serializer.data

        self.assertEqual(data['id'], self.comment_instance.id)
        self.assertEqual(data['name'], self.comment_instance.name)
        self.assertEqual(data['email'], data['email'])
        self.assertEqual(data['body'], self.comment_instance.body)
        self.assertEqual(data['postId'], self.post.pk)
        self.assertNotIn('post', data)

    def test_comment_serializer_deserialization_valid_data(self):
        serializer = CommentSerializer(data=self.valid_comment_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertEqual(serializer.validated_data['post'], self.post)
        self.assertEqual(serializer.validated_data['name'], self.valid_comment_data['name'])
        self.assertEqual(serializer.validated_data['email'], self.valid_comment_data['email'])
        self.assertEqual(serializer.validated_data['body'], self.valid_comment_data['body'])

        self.assertNotIn('postId', serializer.validated_data)

    def test_comment_serializer_deserialization_invalid_data(self):
        serializer = CommentSerializer(data=self.invalid_comment_data)

        self.assertFalse(serializer.is_valid())

        self.assertIn('post', serializer.errors)
        self.assertIn('email', serializer.errors)

    def test_comment_serializer_create_method(self):
        serializer = CommentSerializer(data=self.valid_comment_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        comment = serializer.save()

        self.assertIsNotNone(comment.pk)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.name, self.valid_comment_data['name'])
        self.assertEqual(comment.email, self.valid_comment_data['email'])
        self.assertEqual(comment.body, self.valid_comment_data['body'])

    def test_comment_serializer_update_method(self):
        serializer = CommentSerializer(instance=self.comment_instance, data=self.update_comment_data, partial=True)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated_comment = serializer.save()

        self.comment_instance.refresh_from_db()
        self.assertEqual(self.comment_instance.body, self.update_comment_data['body'])
        self.assertEqual(self.comment_instance.post, self.post)
        self.assertEqual(self.comment_instance.name, 'Existing Comment User')
        self.assertEqual(self.comment_instance.email, 'existing@example.com')
