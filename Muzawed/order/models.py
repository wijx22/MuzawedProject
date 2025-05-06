from django.db import models

from decimal import Decimal
from django.contrib.auth.models import User

from products.models import Product
from accounts.models import SupplierProfile
from accounts.models import SupplierProfile

class Order(models.Model):
    STATUS_CHOICES = [
    ('open', 'مفتوح'),
    ('processing', 'قيد المعالجة'),
    ('closed', 'مستلم'),
    ('cancelled', 'ملغاة'),
    ]


    beneficiary = models.ForeignKey(User, on_delete=models.CASCADE, 
                                    related_name='beneficiary_orders')
    
    supplier = models.ForeignKey(
        SupplierProfile, on_delete=models.CASCADE, related_name='supplier_orders'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_date = models.DateTimeField(blank=True,null=True)
    in_cart = models.BooleanField(default=True)

    def _str_(self):
        return f"Order {self.id} - {self.status}"



class CartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = Decimal(self.quantity) * self.unit_price
        super().save(*args, **kwargs)

    def _str_(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"