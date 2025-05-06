from django.db import models
from order.models import Order


class Payment(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'pending', 'لم يتم الدفع'
        COMPLETED = 'completed', 'مكتمل'
        CANCELLED = 'cancelled', 'ملغى'

    class MethodChoices(models.TextChoices):
        CASH = 'cash', 'نقداً'
        CREDIT = 'credit', 'بطاقة ائتمان'
        DEFERRED = 'deferred', 'دفع آجل'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=MethodChoices.choices,
        default=MethodChoices.CASH
    )

    ref_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_status_display_ar(self):
        return self.StatusChoices(self.status).label

    def __str__(self):
        return f"Order #{self.order.id} - {self.get_status_display_ar()}"
