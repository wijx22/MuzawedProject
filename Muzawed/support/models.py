from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Report(models.Model):
    class StatusChoices(models.TextChoices):
        OPEN = 'open', 'مفتوحة'
        IN_PROGRESS = 'in_progress', 'قيد المراجعة'
        CLOSED = 'closed', 'مغلقة'

    class CategoryChoices(models.TextChoices):
        SUPPLIER = 'supplier', 'ضد المورد'
        PRODUCT = 'product', 'مشكلة في المنتج'
        PAYMENT = 'payment', 'مشكلة في الدفع'
        OTHER = 'other', 'أخرى'


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CategoryChoices.choices, default=CategoryChoices.OTHER)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    attachment = models.FileField(upload_to='report_attachments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20,choices=StatusChoices.choices,default=StatusChoices.OPEN)

    def __str__(self):
        return f"{self.subject} ({self.get_status_display()})"



class ReportReply(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='replies')
    responder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    attachment = models.FileField(upload_to='reply_attachments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"رد على: {self.report.subject} من {self.responder}"

