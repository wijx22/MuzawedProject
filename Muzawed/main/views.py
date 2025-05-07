from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import LoginView
from supplier.models import SupplyDetails, SupplierProfile
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Contact
from products.models import Product, City
import json
from support.models import Report
from django.db.models import Q, Min, Max




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

       
        report = Report.objects.filter(user=request.user).first()

        context = {'supplier': supplier, 'report_id': report.id if report else None}

        return render(request, 'main/supplier_index.html', context)
    else:
        return render(request, 'main/index.html')


def contact_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if not (email and subject and message):
            messages.error(request, 'جميع الحقول مطلوبة.')
        elif len(message.strip()) < 10:
            messages.error(request, 'الرسالة يجب أن تحتوي على 10 أحرف على الأقل.')
        else:
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'صيغة البريد الإلكتروني غير صحيحة.')
                return render(request, 'main/contact.html')

            Contact.objects.create(
                user=request.user if request.user.is_authenticated else None,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'تم إرسال رسالتك بنجاح! سنقوم بالرد عليك قريبًا.')
            return redirect('main:contact_view')

    return render(request, 'main/contact.html')


def about_view(request):
    return render(request, 'main/about.html')




@login_required
def store_status_handler(request):
    if request.method == 'POST':
        supplier_profile = request.user.supplier

        supply_details, _ = SupplyDetails.objects.get_or_create(supplier=supplier_profile)

        from_date = request.POST.get('available_from')
        to_date = request.POST.get('available_to')


        supply_details.unavailable_from = None
        supply_details.unavailable_to = None

        if from_date and to_date:
            try:
         
                from_dt = datetime.strptime(from_date, "%Y-%m-%dT%H:%M")
                to_dt = datetime.strptime(to_date, "%Y-%m-%dT%H:%M")

               
                supply_details.unavailable_from = from_dt
                supply_details.unavailable_to = to_dt

                messages.success(request, f"تم حفظ فترة التوقف من {from_dt} إلى {to_dt} بنجاح.")
            except ValueError:
                messages.error(request, "صيغة التاريخ غير صحيحة. الرجاء التحقق من المدخلات.")
        else:
            messages.info(request, "تمت إزالة فترات التوقف.")

        supply_details.save()
        return redirect('main:index_view')

    return redirect('main:index_view')




def our_suppliers_view(request): 
    category = request.GET.get("category")
    subcategory = request.GET.get("subcategory")
    products = Product.objects.all()

    if category:
        products = products.filter(category=category)

    if subcategory:
        products = products.filter(subcategory=subcategory)

    category_subs = {
        'agricultural': Product.AgriculturalSubcategory.choices,
        'processed': Product.ProcessedFoodSubcategory.choices,
        'industrial': Product.IndustrialSubcategory.choices,
        'special': Product.SpecialProductsSubcategory.choices,
        'miscellaneous': Product.MiscellaneousSubcategory.choices,
    }

    subcategories = category_subs.get(category, [])

    supplier_cities = products.values_list('City', flat=True).distinct()
    suppliers = SupplierProfile.objects.filter(cities_covered__in=supplier_cities).distinct()

    context = {
        'product_categories': Product.ProductCategory.choices,
        'subcategories': subcategories,
        'selected_category': category,
        'selected_subcategory': subcategory,
        'products': products,
        'suppliers': suppliers,
    }

    return render(request, 'main/our_suppliers.html', context)
