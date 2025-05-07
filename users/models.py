from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    street = models.CharField(max_length=255)
    suite = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=20, default="", blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username
