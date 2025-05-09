from django.test import TestCase
from ..models import Album, Photo
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()


class AlbumModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_album', email='album@example.com',
                                             password='123456')

        self.album = Album.objects.create(
            user=self.user,
            title='Test Album Title'
        )

    def test_album_creation(self):
        self.assertIsNotNone(self.album.pk)
        self.assertEqual(self.album.user, self.user)
        self.assertEqual(self.album.title, 'Test Album Title')

    def test_album_user_cannot_be_null(self):
        with self.assertRaises(IntegrityError):
            Album.objects.create(
                user=None,
                title='Album without user'
            )


class PhotoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_photo', email='photo@example.com',
                                             password='123456')
        self.album = Album.objects.create(user=self.user, title='Photo Test Album')

        self.photo = Photo.objects.create(
            album=self.album,
            title='Test Photo Title',
            url='http://example.com/photo.jpg',
            thumbnailUrl='http://example.com/thumb.jpg'
        )

    def test_photo_creation(self):
        self.assertIsNotNone(self.photo.pk)
        self.assertEqual(self.photo.album, self.album)
        self.assertEqual(self.photo.title, 'Test Photo Title')
        self.assertEqual(self.photo.url, 'http://example.com/photo.jpg')
        self.assertEqual(self.photo.thumbnailUrl, 'http://example.com/thumb.jpg')

    def test_photo_album_cannot_be_null(self):
        with self.assertRaises(IntegrityError):
            Photo.objects.create(
                album=None,
                title='Photo without album',
                url='http://example.com/noalbum.jpg'
            )

    def test_photo_thumbnailurl_can_be_blank_and_null(self):
        photo_blank_thumb = Photo.objects.create(
            album=self.album,
            title='Blank Thumb Photo',
            url='http://example.com/blankthumb.jpg',
            thumbnailUrl=''
        )
        self.assertEqual(photo_blank_thumb.thumbnailUrl, '')

        photo_null_thumb = Photo.objects.create(
            album=self.album,
            title='Null Thumb Photo',
            url='http://example.com/nullthumb.jpg',
            thumbnailUrl=None
        )
        self.assertIsNone(photo_null_thumb.thumbnailUrl)
