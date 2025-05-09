from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class PostAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser_post_api', email='postapi@example.com',
                                             password='password123')
        self.client.force_authenticate(user=self.user)
        self.post1 = Post.objects.create(user=self.user, title='Test Post 1 for API', body='Body 1')
        self.post2 = Post.objects.create(user=self.user, title='Test Post 2 for API', body='Body 2')
        self.other_user = User.objects.create_user(username='otheruser_post_api', email='otherpostapi@example.com',
                                                   password='password456')
        self.other_post = Post.objects.create(user=self.other_user, title='Other User Post', body='Other body')
        self.list_url = reverse('post-list')
        self.detail_url = reverse('post-detail', kwargs={'pk': self.post1.pk})
        self.other_detail_url = reverse('post-detail', kwargs={'pk': self.other_post.pk})

    def test_list_posts(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Post.objects.filter(user=self.user).count())
        for post_data in response.data:
            self.assertEqual(post_data['userId'], self.user.pk)

    def test_list_posts_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_post(self):
        new_post_data = {
            'user': self.user.pk,
            'title': 'New Test Post from API',
            'body': 'Body of new post.',
        }
        response = self.client.post(self.list_url, data=new_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 4)
        new_post = Post.objects.get(title='New Test Post from API')
        self.assertEqual(new_post.user, self.user)
        self.assertEqual(new_post.title, new_post_data['title'])
        self.assertEqual(new_post.body, new_post_data['body'])

    def test_create_post_unauthenticated(self):
        self.client.force_authenticate(user=None)
        new_post_data = {'title': 'Unauthorized Post', 'body': 'Unauthorized Body'}
        response = self.client.post(self.list_url, data=new_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_post(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.post1.pk)
        self.assertEqual(response.data['title'], self.post1.title)
        self.assertEqual(response.data['body'], self.post1.body)
        self.assertEqual(response.data['userId'], self.user.pk)

    def test_retrieve_other_users_post(self):
        response = self.client.get(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post(self):
        update_data = {
            'user': self.user.pk,
            'title': 'Updated Test Post via API',
            'body': 'Updated body of post.',
        }
        response = self.client.put(self.detail_url, data=update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, update_data['title'])
        self.assertEqual(self.post1.body, update_data['body'])
        self.assertEqual(self.post1.user, self.user)

    def test_update_other_users_post(self):
        update_data = {'title': 'Attempted Update', 'body': 'Attempted Body'}
        response = self.client.put(self.other_detail_url, data=update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.other_post.refresh_from_db()
        self.assertNotEqual(self.other_post.title, update_data['title'])

    def test_delete_post(self):
        post_to_delete_pk = self.post2.pk
        delete_url = reverse('post-detail', kwargs={'pk': post_to_delete_pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 2)
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=post_to_delete_pk)

    def test_delete_other_users_post(self):
        response = self.client.delete(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), 3)
        self.assertTrue(Post.objects.filter(pk=self.other_post.pk).exists())


class CommentAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser_comment_api', email='commentapi@example.com',
                                             password='password123')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(user=self.user, title='Test Post for Comments', body='Body for comments.')
        self.comment1 = Comment.objects.create(post=self.post, name='User 1', email='user1@example.com',
                                               body='Test Comment 1 for API')
        self.comment2 = Comment.objects.create(post=self.post, name='User 2', email='user2@example.com',
                                               body='Test Comment 2 for API')
        self.other_user = User.objects.create_user(username='otheruser_comment_api',
                                                   email='othercommentapi@example.com', password='password789')
        self.other_post = Post.objects.create(user=self.other_user, title='Other User Post for Comments',
                                              body='Other body for comments.')
        self.other_comment = Comment.objects.create(post=self.other_post, name='Other User', email='other@example.com',
                                                    body='Other User Comment')
        self.list_url = reverse('comment-list')
        self.detail_url = reverse('comment-detail', kwargs={'pk': self.comment1.pk})
        self.other_detail_url = reverse('comment-detail', kwargs={'pk': self.other_comment.pk})

    def test_list_comments(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Comment.objects.filter(post__user=self.user).count())

    def test_list_comments_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_comment(self):
        new_comment_data = {
            'post': self.post.pk,
            'name': 'New Commenter',
            'email': 'new@example.com',
            'body': 'Body of new comment.',
        }
        response = self.client.post(self.list_url, data=new_comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Comment.objects.count(), 4)
        new_comment = Comment.objects.get(name='New Commenter')
        self.assertEqual(new_comment.post, self.post)
        self.assertEqual(new_comment.name, new_comment_data['name'])
        self.assertEqual(new_comment.email, new_comment_data['email'])
        self.assertEqual(new_comment.body, new_comment_data['body'])

    def test_create_comment_unauthenticated(self):
        self.client.force_authenticate(user=None)
        new_comment_data = {
            'post': self.post.pk,
            'name': 'Unauthorized Commenter',
            'email': 'unauth@example.com',
            'body': 'Unauthorized Body'
        }
        response = self.client.post(self.list_url, data=new_comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_comment_on_other_users_post(self):
        create_data_on_other_post = {
            'post': self.other_post.pk,
            'name': 'Commenter on Other Post',
            'email': 'onother@example.com',
            'body': 'Comment on other users post.'
        }
        response = self.client.post(self.list_url, data=create_data_on_other_post, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Comment.objects.filter(name='Commenter on Other Post').exists())

    def test_retrieve_comment(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.comment1.pk)
        self.assertEqual(response.data['name'], self.comment1.name)
        self.assertEqual(response.data['email'], self.comment1.email)
        self.assertEqual(response.data['body'], self.comment1.body)
        self.assertEqual(response.data['postId'], self.post.pk)

    def test_retrieve_other_users_comment(self):
        response = self.client.get(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_comment(self):
        update_data = {
            'post': self.post.pk,
            'name': 'Updated Commenter',
            'email': 'updated@example.com',
            'body': 'Updated body of comment.',
        }
        response = self.client.put(self.detail_url, data=update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.comment1.refresh_from_db()
        self.assertEqual(self.comment1.name, update_data['name'])
        self.assertEqual(self.comment1.email, update_data['email'])
        self.assertEqual(self.comment1.body, update_data['body'])
        self.assertEqual(self.comment1.post, self.post)

    def test_update_other_users_comment(self):
        update_data = {'name': 'Attempted Update', 'body': 'Attempted Body'}
        response = self.client.put(self.other_detail_url, data=update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.other_comment.refresh_from_db()
        self.assertNotEqual(self.other_comment.name, update_data['name'])

    def test_delete_comment(self):
        comment_to_delete_pk = self.comment2.pk
        delete_url = reverse('comment-detail', kwargs={'pk': comment_to_delete_pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 2)
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=comment_to_delete_pk)

    def test_delete_other_users_comment(self):
        response = self.client.delete(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Comment.objects.count(), 3)
        self.assertTrue(Comment.objects.filter(pk=self.other_comment.pk).exists())
