from django.db import models
from django.contrib.auth.models import AbstractUser

class Member(AbstractUser):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    deskripsi = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Transaction #{self.pk} - Member: {self.member.username} - Amount: {self.total_amount}'

class TransactionItem(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=0)

    def __str__(self):
        return f'Transaction Item - Transaction: {self.transaction.pk} - Product: {self.product.name}'

    def subtotal(self):
        return self.quantity * self.price
