# accounts/models.py
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name
