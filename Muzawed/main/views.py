from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from .models import Contact

def index_view(request):
    return render(request, 'main/index.html')



def contact_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if email and subject and message:
            contact = Contact.objects.create(
                user=request.user if request.user.is_authenticated else None,
                email=email,
                subject=subject,
                message=message
            )
            contact.save()
            messages.success(request, 'تم إرسال رسالتك بنجاح! سنقوم بالرد عليك قريبًا.')
            return redirect('main:contact_view')
        else:
            messages.error(request, 'يرجى تعبئة جميع الحقول.')

    return render(request, 'main/contact.html')
