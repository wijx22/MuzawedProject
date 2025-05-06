from django.db import models
from order.models import Order

# Create your models here.



class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'لم يتم الدفع'),
            ('completed', 'مكتمل'),
            ('cancelled', 'ملغى')
        ],
        default='pending'
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('cash', 'نقدا'),
            ('credit', 'بطاقة ائتمان'),
            ('deferred', 'دفع آجل')
        ],
        default='cash'
    )

    ref_id = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment #{self.id} for Order #{self.order.id} - {self.status}"
    

    def get_status_in_arabic(self):
        status_dict = {
            'pending': 'لم يتم الدفع',
            'completed': 'مكتمل',
            'cancelled': 'ملغى'
        }
        return status_dict.get(self.status, self.status)
    
