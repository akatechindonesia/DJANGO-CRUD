from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    deskripsi = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True)

    def __str__(self):
        return self.name