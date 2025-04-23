from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=255)
    store_description = models.TextField()
    status = models.CharField(
        choices=[("active", "Active"), ("inactive", "Inactive")], max_length=10
    )
    supply_sector = models.CharField(
        max_length=50,
        choices=[("retail", "Retail"), ("wholesale", "Wholesale"), ("both", "Both")],
    )
    delivery_service = models.CharField(
        max_length=50,
        choices=[("fast", "Fast"), ("shipping", "Shipping"), ("both", "Both")],
    )
    fast_service_details = models.CharField(max_length=255, blank=True)
    order_lead_time_days = models.IntegerField()
    late_payment_options = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    unavailable_from = models.DateTimeField(null=True, blank=True)
    unavailable_to = models.DateTimeField(null=True, blank=True)
    store_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    official_holidays = models.CharField(max_length=50)

    def __str__(self):
        return (
            f"{self.user.username} - {self.store_type.title()} ({self.status.title()})"
        )


CATEGORY_TYPE_CHOICES = []

PRODUCT_SUBCATEGORY_CHOICES = []


class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to="Media/")
    min_stock_alert = models.IntegerField(default=0)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES)
    product_subcategory = models.CharField(
        max_length=20, choices=PRODUCT_SUBCATEGORY_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category_type}) - {self.supplier.user.username}"


class Branch(models.Model):
    supplier = models.ForeignKey(
        Supplier, related_name="branches", on_delete=models.CASCADE
    )
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.supplier.user.username} - {self.city}"
