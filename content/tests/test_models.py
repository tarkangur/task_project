from django.test import TestCase

from ..models import Post, Comment

from django.contrib.auth import get_user_model

User = get_user_model()

from django.db.utils import IntegrityError


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser_post_model', email='postmodel@example.com',
                                             password='password123')

        self.post = Post.objects.create(
            user=self.user,
            title='Test Post Title',
            body='This is the body of the test post.'
        )

    def test_post_creation(self):
        self.assertIsNotNone(self.post.pk)
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.title, 'Test Post Title')
        self.assertEqual(self.post.body, 'This is the body of the test post.')

    def test_post_str_method(self):
        self.assertEqual(str(self.post), 'Test Post Title')

    def test_post_user_cannot_be_null(self):
        with self.assertRaises(IntegrityError):
            Post.objects.create(
                user=None,
                title='Post without user',
                body='Body without user'
            )


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser_comment_model', email='commentmodel@example.com',
                                             password='password123')
        self.post = Post.objects.create(user=self.user, title='Comment Test Post', body='Body for comment test.')

        # Comment modelinde user alanı yok, bu yüzden user=self.user kaldırıldı
        self.comment = Comment.objects.create(
            post=self.post,
            name='Test User Name',  # Comment modelindeki name alanı
            email='test@example.com',
            body='This is a test comment body.'
        )

    def test_comment_creation(self):
        self.assertIsNotNone(self.comment.pk)
        self.assertEqual(self.comment.post, self.post)
        # Comment modelinde user alanı yok, bu yüzden bu assert kaldırıldı
        # self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.name, 'Test User Name')  # name alanını kontrol et
        self.assertEqual(self.comment.email, 'test@example.com')  # email alanını kontrol et
        self.assertEqual(self.comment.body, 'This is a test comment body.')

    def test_comment_str_method(self):
        self.assertEqual(str(self.comment), 'Test User Name')  # name alanına göre düzeltildi

    def test_comment_post_cannot_be_null(self):
        with self.assertRaises(IntegrityError):
            Comment.objects.create(
                post=None,
                name='No Post Comment',
                email='nopost@example.com',
                body='Comment without post'
            )
