from .models import Notification

def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).order_by('-created_at')[:5]
        return {'notifications': notifications}
    return {}
