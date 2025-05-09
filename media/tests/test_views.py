from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Album, Photo
from django.contrib.auth import get_user_model

User = get_user_model()


class AlbumAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser_album_api', email='albumapi@example.com', password='password123')

        self.client.force_authenticate(user=self.user)

        self.album1 = Album.objects.create(user=self.user, title='Test Album 1 for API')
        self.album2 = Album.objects.create(user=self.user, title='Test Album 2 for API')

        self.other_user = User.objects.create_user(username='otheruser_album_api', email='otheralbumapi@example.com', password='password456')
        self.other_album = Album.objects.create(user=self.other_user, title='Other User Album')

        self.list_url = reverse('album-list')

        self.detail_url = reverse('album-detail', kwargs={'pk': self.album1.pk})

        self.other_detail_url = reverse('album-detail', kwargs={'pk': self.other_album.pk})

    def test_list_albums(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), Album.objects.filter(user=self.user).count())

        for album_data in response.data:
             self.assertEqual(album_data['userId'], self.user.pk)

    def test_list_albums_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_album(self):
        new_album_data = {
            'title': 'New Test Album from API',
        }

        response = self.client.post(self.list_url, data=new_album_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        self.assertEqual(Album.objects.count(), 4)

        new_album = Album.objects.get(title='New Test Album from API')
        self.assertEqual(new_album.user, self.user)
        self.assertEqual(new_album.title, new_album_data['title'])

    def test_create_album_unauthenticated(self):
        self.client.force_authenticate(user=None)
        new_album_data = {'title': 'Unauthorized Album'}
        response = self.client.post(self.list_url, data=new_album_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_album(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], self.album1.pk)
        self.assertEqual(response.data['title'], self.album1.title)
        self.assertEqual(response.data['userId'], self.user.pk)

    def test_retrieve_other_users_album(self):
        response = self.client.get(self.other_detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_album(self):
        update_data = {
            'title': 'Updated Test Album via API',
        }

        response = self.client.put(self.detail_url, data=update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        self.album1.refresh_from_db()
        self.assertEqual(self.album1.title, update_data['title'])
        self.assertEqual(self.album1.user, self.user)

    def test_update_other_users_album(self):
        update_data = {'title': 'Attempted Update'}
        response = self.client.put(self.other_detail_url, data=update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.other_album.refresh_from_db()
        self.assertNotEqual(self.other_album.title, update_data['title'])

    def test_delete_album(self):
        album_to_delete_pk = self.album2.pk
        delete_url = reverse('album-detail', kwargs={'pk': album_to_delete_pk})

        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Album.objects.count(), 2)

        with self.assertRaises(Album.DoesNotExist):
            Album.objects.get(pk=album_to_delete_pk)

    def test_delete_other_users_album(self):
        response = self.client.delete(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Album.objects.count(), 3)
        self.assertTrue(Album.objects.filter(pk=self.other_album.pk).exists())


class PhotoAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser_photo_api', email='photoapi@example.com', password='password123')
        self.album = Album.objects.create(user=self.user, title='Photo Test Album for API')

        self.client.force_authenticate(user=self.user)

        self.photo1 = Photo.objects.create(album=self.album, title='Test Photo 1 for API', url='http://example.com/p1.jpg')
        self.photo2 = Photo.objects.create(album=self.album, title='Test Photo 2 for API', url='http://example.com/p2.jpg')

        self.other_user = User.objects.create_user(username='otheruser_photo_api', email='otherphotoapi@example.com', password='password789')
        self.other_album = Album.objects.create(user=self.other_user, title='Other User Photo Album')
        self.other_photo = Photo.objects.create(album=self.other_album, title='Other User Photo', url='http://example.com/other.jpg')

        self.list_url = reverse('photo-list')

        self.detail_url = reverse('photo-detail', kwargs={'pk': self.photo1.pk})

        self.other_detail_url = reverse('photo-detail', kwargs={'pk': self.other_photo.pk})

    def test_list_photos(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_photo_count = Photo.objects.filter(album__user=self.user).count()
        self.assertEqual(len(response.data), user_photo_count)

        for photo_data in response.data:
             album_of_photo = Album.objects.get(pk=photo_data['albumId'])
             self.assertEqual(album_of_photo.user, self.user)

    def test_list_photos_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_photo(self):
        new_photo_data = {
            'album': self.album.pk,
            'title': 'New Test Photo from API',
            'url': 'http://example.com/new_photo.jpg',
            'thumbnailUrl': 'http://example.com/new_photo_thumb.jpg'
        }

        response = self.client.post(self.list_url, data=new_photo_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        self.assertEqual(Photo.objects.count(), 4)

        new_photo = Photo.objects.get(title='New Test Photo from API')
        self.assertEqual(new_photo.album, self.album)
        self.assertEqual(new_photo.title, new_photo_data['title'])
        self.assertEqual(new_photo.url, new_photo_data['url'])

    def test_create_photo_unauthenticated(self):
        self.client.force_authenticate(user=None)
        new_photo_data = {
            'album': self.album.pk,
            'title': 'Unauthorized Photo',
            'url': 'http://example.com/unauth.jpg'
        }
        response = self.client.post(self.list_url, data=new_photo_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_photo_in_other_users_album(self):
        create_data_in_other_album = {
            'album': self.other_album.pk,
            'title': 'Photo in Other Album',
            'url': 'http://example.com/in_other_album.jpg'
        }

        response = self.client.post(self.list_url, data=create_data_in_other_album, format='json')

        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN])

    def test_retrieve_photo(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], self.photo1.pk)
        self.assertEqual(response.data['title'], self.photo1.title)
        self.assertEqual(response.data['url'], self.photo1.url)
        self.assertEqual(response.data['albumId'], self.album.pk)

    def test_retrieve_other_users_photo(self):
        response = self.client.get(self.other_detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_photo(self):
        update_data = {
            'album': self.album.pk,
            'title': 'Updated Test Photo via API',
            'url': 'http://example.com/updated_p1.jpg',
            'thumbnailUrl': 'http://example.com/updated_p1_thumb.jpg'
        }

        response = self.client.put(self.detail_url, data=update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        self.photo1.refresh_from_db()
        self.assertEqual(self.photo1.title, update_data['title'])
        self.assertEqual(self.photo1.url, update_data['url'])
        self.assertEqual(self.photo1.thumbnailUrl, update_data['thumbnailUrl'])
        self.assertEqual(self.photo1.album, self.album)

    def test_update_other_users_photo(self):
        update_data = {'title': 'Attempted Photo Update', 'url': 'http://example.com/attempted.jpg'}
        response = self.client.put(self.other_detail_url, data=update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.other_photo.refresh_from_db()
        self.assertNotEqual(self.other_photo.title, update_data['title'])

    def test_delete_photo(self):
        photo_to_delete_pk = self.photo2.pk
        delete_url = reverse('photo-detail', kwargs={'pk': photo_to_delete_pk})

        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Photo.objects.count(), 2)

        with self.assertRaises(Photo.DoesNotExist):
            Photo.objects.get(pk=photo_to_delete_pk)

    def test_delete_other_users_photo(self):
        response = self.client.delete(self.other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Photo.objects.count(), 3)
        self.assertTrue(Photo.objects.filter(pk=self.other_photo.pk).exists())
