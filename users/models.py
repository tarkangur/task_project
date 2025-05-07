from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    street = models.CharField(max_length=255)
    suite = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField(null=True)
    geo_lat = models.FloatField(null=True)
    geo_lang = models.FloatField(null=True)
    phone = models.CharField(max_length=20, default="")
    website = models.URLField(max_length=255, null=True)
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.username
