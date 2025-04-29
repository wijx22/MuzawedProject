from django.db import models
from accounts.models import SupplierProfile


class SupplyDetails(models.Model):
    supplier =models.OneToOneField(SupplierProfile,on_delete=models.CASCADE, related_name="supply_details")
    logo = models.ImageField(upload_to="supplier_logos/", null=True, blank=True)
    supply_sector = models.CharField(
        max_length=50,
        choices=[
            ("retail", "بيع بالتجزئة"),
            ("wholesale", "بالجملة"),
            ("both", "كلاهما"),
        ],
    )
    delivery_service = models.CharField(
        max_length=50,
        choices=[("fast", "سريع"), ("shipping", "شحن"), ("both", "كلاهما")],
    )

    order_lead_time_days = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    unavailable_from = models.DateTimeField(null=True, blank=True)
    unavailable_to = models.DateTimeField(null=True, blank=True)
    fast_service_details = models.IntegerField(null=True, blank=True)
    late_payment_options = models.BooleanField(default=False)
    supply_days = models.CharField(
        max_length=6,
        help_text="Days the supplier is available to supply (e.g., 'Saturday to Thursday')",
    )
    supply_type = models.CharField(
        max_length=50,
        choices=[
            ("on_demand", "حسب الطلب"),
            ("scheduled", "مجدول"),
            ("both", "كلاهما"),
        ],
        default="scheduled",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        return "/static/images/placeholder.svg"

    def __str__(self):
        return (
            f"{self.supplier.name} - supply details "
        )



class City(models.Model):
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
    
    name = models.CharField(
        max_length=50,
        choices=CityChoices.choices,
        default=CityChoices.RIYADH,  
    )

    # Many-to-many relationship for suppliers
    suppliers = models.ManyToManyField(SupplierProfile,related_name="cities_covered")

    def __str__(self):
        return self.name

    city = models.CharField(max_length=100, choices=CityChoices.choices)

    def __str__(self):
        return f"{self.supplier.name} - {self.city}"


class CommercialInfo(models.Model):
    supplier =models.OneToOneField(SupplierProfile,on_delete=models.CASCADE, related_name="commercial_info")

    # Basic Business Info
    store_name = models.CharField(max_length=255)
    store_description = models.TextField()
    # Legal Docs
    registration_document = models.FileField(
        upload_to="Media/commercial_documents/", null=True, blank=True
    )
    license_document = models.FileField(
        upload_to="Media/commercial_documents/", null=True, blank=True
    )
    tax_certificate = models.FileField(
        upload_to="Media/commercial_documents/", null=True, blank=True
    )

    # Bank Details
    bank_account_name = models.CharField(max_length=255)
    bank_account_number = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    iban = models.CharField(max_length=34, blank=True, null=True)
    swift_code = models.CharField(max_length=11, blank=True, null=True)

    # Contact & Representative Info
    commercial_contact_name = models.CharField(max_length=100, blank=True, null=True)
    commercial_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    commercial_contact_email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.supplier.user.username} - Commercial Info"




class SupplyRequest(models.Model):
    commercialInfo = models.ForeignKey(CommercialInfo, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=250)
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('accepted', 'مقبولة'),
        ('rejected', 'مرفوضة'),
    ]
    
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending')

