from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import LoginView
from supplier.models import SupplyDetails, SupplierProfile
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from supplier.models import SupplyDetails, SupplierProfile 

from .models import Contact

#def index_view(request):
#    if hasattr(request.user, 'supplier'):
#
#        return render(request, 'main/supplier_index.html')
#    
#
#    else:
#        return render(request, 'main/index.html')

def index_view(request):
    if hasattr(request.user, 'supplier'):
        supplier = request.user.supplier
        return render(request, 'main/supplier_index.html', {'supplier': supplier})
    else:
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

@login_required
def store_status_handler(request):
    if request.method == 'POST':
        supplier_profile = request.user.supplierprofile

        supply_details, _ = SupplyDetails.objects.get_or_create(supplier=supplier_profile)


        from_date = request.POST.get('available_from')
        to_date = request.POST.get('available_to')

        # إعادة تعيين القيم
        supply_details.unavailable_from = None
        supply_details.unavailable_to = None

        if from_date and to_date:
            supply_details.unavailable_from = from_date
            supply_details.unavailable_to = to_date
            messages.success(request, "تم حفظ فترة التوقف بنجاح.")
        else:
            messages.info(request, "تم مسح فترات التوقف الحالية.")

        supply_details.save()
        return redirect('supplier:dashboard')  # غيّريه إذا تبين ترجعي لمكان مختلف

    return redirect('supplier:dashboard')
