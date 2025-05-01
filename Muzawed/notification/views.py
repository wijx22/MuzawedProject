from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect(request.GET.get('next', '/'))

