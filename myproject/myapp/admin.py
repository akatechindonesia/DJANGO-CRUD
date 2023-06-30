from django.contrib import admin
from .models import Member, Product, Transaction, TransactionItem

admin.site.register(Member)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(TransactionItem)
