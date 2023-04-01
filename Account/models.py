# accounts/models.py

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True)
    city_town = models.CharField(max_length=50)
    postcode_zip = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=10)
    nid_number = models.CharField(max_length=20, blank=True)
    additional_information = models.TextField(blank=True)
    
    def __str__(self):
        return self.user
