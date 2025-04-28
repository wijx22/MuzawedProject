from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import LoginView

from .models import Contact

def index_view(request):
    print(hasattr(request.user, 'supplierprofile'))
    if hasattr(request.user, 'supplierprofile'):

        return redirect("main:supplie_view")

    return render(request, 'main/index.html')

def contact_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if email and subject and message:
            Contact.objects.create(
                user=request.user if request.user.is_authenticated else None,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'تم إرسال رسالتك بنجاح! سنقوم بالرد عليك قريبًا.')
            return redirect('main:contact_view')
        else:
            messages.error(request, 'يرجى تعبئة جميع الحقول.')

    return render(request, 'main/contact.html')

def about_view(request):
    return render(request, 'main/about.html')

def supplie_view(request):
    if hasattr(request.user, 'supplierprofile'):
        return render(request, 'main/supplier_index.html')
    else:
        return redirect('main:index_view')  
    