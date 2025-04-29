from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=[
        ('order', 'Order Notification'),
        ('message', 'Message Notification'),
        ('alert', 'Alert Notification'),
    ])
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.recipient.username} - {self.notification_type}"
