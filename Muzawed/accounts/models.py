from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ProfileBeneficiary(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'

    class CityChoices(models.TextChoices):
        RIYADH = "riyadh", "الرياض"
        JEDDAH = "jeddah", "جدة"
        MECCA = "mecca", "مكة"
        MEDINA = "medina", "المدينة"
        DAMMAM = "dammam", "الدمام"
        KHOBAR = "khobar", "الخبر"
        TABUK = "tabuk", "تبوك"
        ABHA = "abha", "أبها"
        HAIL = "hail", "حائل"
        NAJRAN = "najran", "نجران"

    user = models.OneToOneField(User, on_delete=models.CASCADE ,related_name='customer')
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    city = models.CharField(max_length=20, choices=CityChoices.choices, default=CityChoices.RIYADH)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class SupplierProfile(models.Model):
    class RequestStatusChoises(models.TextChoices):
       NO_REQUEST="No-request","لا يوجد طلب"
       REJECTED= "Rejected", "مرفوض"
       ACCEPTED= "Accepted", "مقبول"
       PENDING= "Pending", "قيد المعالجة"
    
    status = models.CharField(
        max_length=10,
        choices=RequestStatusChoises.choices,
        default=RequestStatusChoises.NO_REQUEST,
    )
    rejection_reason = models.TextField(blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE ,related_name='supplier')
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)  



    



