from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to="supplier_logos/", null=True, blank=True)
    status = models.CharField(
        choices=[("active", "متاح"), ("inactive", "غير متاح")], max_length=10
    )
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
    order_lead_time_days = models.IntegerField()
    is_available = models.BooleanField(default=True)
    unavailable_from = models.DateTimeField(null=True, blank=True)
    unavailable_to = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    official_holidays = models.CharField(max_length=50)

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        return None

    def __str__(self):
        return (
            f"{self.user.username} - {self.store_type.title()} ({self.status.title()})"
        )


class Branch(models.Model):
    supplier = models.ManyToManyField(
        Supplier, related_name="branches"
    )
    city = models.CharField(max_length=100)

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
        upload_to="commercial_documents/", null=True, blank=True
    )
    license_document = models.FileField(
        upload_to="commercial_documents/", null=True, blank=True
    )
    tax_certificate = models.FileField(
        upload_to="commercial_documents/", null=True, blank=True
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

    # Status
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.supplier.user.username} - Commercial Info"


class SupplyMethod(models.Model):
    supplier = models.OneToOneField(
        Supplier, on_delete=models.CASCADE, related_name="supply_method"
    )
    fast_service_details = models.CharField(max_length=255, blank=True)
    late_payment_options = models.BooleanField(default=False)
    supply_days = models.CharField(
        max_length=100,
        help_text="Days the supplier is available to supply (e.g., 'Saturday to Thursday')",
    )
    supply_type = models.CharField(
        max_length=50,
        choices=[
            ("on_demand", "On-Demand"),
            ("scheduled", "Scheduled"),
            ("both", "Both"),
        ],
        default="scheduled",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.supplier.user.username} - Supply Method"
