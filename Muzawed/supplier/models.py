from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to="Media/supplier_logos/", null=True, blank=True)
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
    fast_service_details = models.CharField(max_length=255, blank=True)
    late_payment_options = models.BooleanField(default=False)
    supply_days = models.CharField(
        max_length=6,
        help_text="Days the supplier is available to supply (e.g., 'Saturday to Thursday')",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rejection_reason = models.TextField(blank=True, null=True)

    STATUS_CHOICES = [
        ("rejected", "رفض"),
        ("accepted", "مقبول"),
        ("pending", "قيد المعالجة"),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
    )

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        return "/static/images/placeholder.svg"

    def __str__(self):
        return (
            f"{self.user.username} - {self.store_type.title()} ({self.status.title()})"
        )


class Branch(models.Model):
    CITY_CHOICES = [
        ("riyadh", "الرياض"),
        ("jeddah", "جدة"),
        ("mecca", "مكة"),
        ("medina", "المدينة"),
        ("dammam", "الدمام"),
        ("khobar", "الخبر"),
        ("tabuk", "تبوك"),
        ("abha", "أبها"),
        ("hail", "حائل"),
        ("najran", "نجران"),
    ]
    supplier = models.ForeignKey(
        Supplier, related_name="branches", on_delete=models.CASCADE
    )
    city = models.CharField(max_length=100, choices=CITY_CHOICES)

    def __str__(self):
        return f"{self.supplier.user.username} - {self.city}"


class CommercialInfo(models.Model):
    supplier = models.OneToOneField(
        Supplier, on_delete=models.CASCADE, related_name="commercial_info"
    )
    # Basic Business Info
    store_description = models.TextField()
    store_name = models.CharField(max_length=255)
    store_address = models.CharField(max_length=255)
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

    # Status reson add this?
    #is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.supplier.user.username} - Commercial Info"


class SupplyDetail(models.Model):
    supplier = models.OneToOneField(
        Supplier, on_delete=models.CASCADE, related_name="supply_detail"
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

    def __str__(self):
        return f"{self.supplier.user.username} - Supply Detail"




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

