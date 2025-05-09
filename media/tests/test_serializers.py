from django.test import TestCase
from ..serializers import AlbumSerializer, PhotoSerializer
from ..models import Album, Photo
from django.contrib.auth import get_user_model

User = get_user_model()


class AlbumSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser_album_serializer', email='albumserializer@example.com',
                                             password='password123')

        self.album_instance = Album.objects.create(
            user=self.user,
            title='Existing Album for Serialization'
        )

        self.valid_album_data = {
            'user': self.user.pk,
            'title': 'New Album from Test Data'
        }

        self.invalid_album_data = {
            'title': 'Album without User'
        }

        self.update_album_data = {
            'title': 'Updated Album Title'
        }

    def test_album_serializer_serialization(self):
        serializer = AlbumSerializer(instance=self.album_instance)
        data = serializer.data

        self.assertEqual(data['id'], self.album_instance.id)
        self.assertEqual(data['title'], self.album_instance.title)
        self.assertEqual(data['userId'], self.user.pk)
        self.assertNotIn('user', data)
    def test_album_serializer_deserialization_valid_data(self):
        serializer = AlbumSerializer(data=self.valid_album_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['user'],
                         self.user)
        self.assertEqual(serializer.validated_data['title'], self.valid_album_data['title'])
        self.assertNotIn('userId', serializer.validated_data)
    def test_album_serializer_deserialization_invalid_data(self):
        serializer = AlbumSerializer(data=self.invalid_album_data)

        self.assertFalse(serializer.is_valid())

        self.assertIn('user', serializer.errors)
        self.assertNotIn('title', serializer.errors)

        self.assertNotIn('userId', serializer.errors)

    def test_album_serializer_create_method(self):
        serializer = AlbumSerializer(data=self.valid_album_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        album = serializer.save()

        self.assertIsNotNone(album.pk)

        self.assertEqual(album.user, self.user)
        self.assertEqual(album.title, self.valid_album_data['title'])

    def test_album_serializer_update_method(self):
        serializer = AlbumSerializer(instance=self.album_instance, data=self.update_album_data, partial=True)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated_album = serializer.save()

        self.album_instance.refresh_from_db()
        self.assertEqual(self.album_instance.title, self.update_album_data['title'])
        self.assertEqual(self.album_instance.user, self.user)


# PhotoSerializer için test sınıfı
class PhotoSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser_photo_serializer', email='photoserializer@example.com',
                                             password='password123')
        self.album = Album.objects.create(user=self.user, title='Photo Test Album for Serializer')

        self.photo_instance = Photo.objects.create(
            album=self.album,
            title='Existing Photo for Serialization',
            url='http://example.com/existing.jpg',
            thumbnailUrl='http://example.com/existing_thumb.jpg'
        )

        self.valid_photo_data = {
            'album': self.album.pk,
            'title': 'New Photo from Test Data',
            'url': 'http://example.com/new.jpg',
            'thumbnailUrl': 'http://example.com/new_thumb.jpg'
        }

        self.invalid_photo_data = {
            'thumbnailUrl': 'http://example.com/invalid_thumb.jpg'
        }

        self.update_photo_data = {
            'title': 'Updated Photo Title',
            'url': 'http://example.com/updated.jpg',
            'thumbnailUrl': None
        }
    def test_photo_serializer_serialization(self):
        serializer = PhotoSerializer(instance=self.photo_instance)
        data = serializer.data

        self.assertEqual(data['id'], self.photo_instance.id)
        self.assertEqual(data['title'], self.photo_instance.title)
        self.assertEqual(data['url'], self.photo_instance.url)
        self.assertEqual(data['thumbnailUrl'], self.photo_instance.thumbnailUrl)

        self.assertEqual(data['albumId'], self.album.pk)
        self.assertNotIn('album', data)

    def test_photo_serializer_deserialization_valid_data(self):
        serializer = PhotoSerializer(data=self.valid_photo_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        self.assertEqual(serializer.validated_data['album'],
                         self.album)
        self.assertEqual(serializer.validated_data['title'], self.valid_photo_data['title'])
        self.assertEqual(serializer.validated_data['url'], self.valid_photo_data['url'])
        self.assertEqual(serializer.validated_data['thumbnailUrl'], self.valid_photo_data['thumbnailUrl'])

        self.assertNotIn('albumId', serializer.validated_data)

    def test_photo_serializer_deserialization_invalid_data(self):
        serializer = PhotoSerializer(data=self.invalid_photo_data)

        self.assertFalse(serializer.is_valid())

        self.assertIn('album', serializer.errors)
        self.assertIn('title', serializer.errors)
        self.assertIn('url', serializer.errors)
        self.assertNotIn('thumbnailUrl', serializer.errors)

        self.assertNotIn('albumId', serializer.errors)

    def test_photo_serializer_create_method(self):
        serializer = PhotoSerializer(data=self.valid_photo_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        photo = serializer.save()

        self.assertIsNotNone(photo.pk)

        self.assertEqual(photo.album, self.album)
        self.assertEqual(photo.title, self.valid_photo_data['title'])
        self.assertEqual(photo.url, self.valid_photo_data['url'])
        self.assertEqual(photo.thumbnailUrl, self.valid_photo_data['thumbnailUrl'])

    def test_photo_serializer_update_method(self):
        serializer = PhotoSerializer(instance=self.photo_instance, data=self.update_photo_data, partial=True)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        updated_photo = serializer.save()

        self.photo_instance.refresh_from_db()
        self.assertEqual(self.photo_instance.title, self.update_photo_data['title'])
        self.assertEqual(self.photo_instance.url, self.update_photo_data['url'])
        self.assertEqual(self.photo_instance.thumbnailUrl,
                         self.update_photo_data['thumbnailUrl'])
        self.assertEqual(self.photo_instance.album, self.album)

