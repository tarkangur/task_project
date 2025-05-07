from django.db import models
from django.conf import settings


class Album(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="albums")
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="photos")
    title = models.CharField(max_length=150)
    url = models.URLField()
    thumbnailUrl = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
