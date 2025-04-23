from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProfileBeneficiary(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class SupplierProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=255)
    store_description = models.TextField()
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    SUPPLY_SECTOR_CHOICES = [
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
        ('both', 'Both'),
    ]
    supply_sector = models.CharField(max_length=50, choices=SUPPLY_SECTOR_CHOICES)

    DELIVERY_SERVICE_CHOICES = [
        ('fast', 'Fast'),
        ('shipping', 'Shipping'),
        ('both', 'Both'),
    ]
    delivery_service = models.CharField(max_length=50, choices=DELIVERY_SERVICE_CHOICES)

    fast_service_details = models.CharField(max_length=255, blank=True)
    order_lead_time_days = models.IntegerField()
    late_payment_options = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    unavailable_from = models.DateTimeField(null=True, blank=True)
    unavailable_to = models.DateTimeField(null=True, blank=True)

    STORE_TYPE_CHOICES = [
        ('factory', 'Factory'),
        ('farm', 'Farm'),
        ('company', 'Company'),
    ]
    store_type = models.CharField(max_length=50, choices=STORE_TYPE_CHOICES)

    official_holidays = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.store_type}"
