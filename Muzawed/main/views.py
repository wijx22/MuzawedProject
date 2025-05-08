from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import LoginView
from supplier.models import SupplyDetails, SupplierProfile
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from supplier.models import SupplyDetails, SupplierProfile 
from datetime import datetime
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Contact
from products.models import Product, City
import json
from support.models import Report
from django.db.models import Q, Min, Max

from django.shortcuts import render
from products.models import  CategoryImage


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
    suppliers = SupplierProfile.objects.all()
    products = Product.objects.all()

    # Get filter parameters from the request
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    delivery_type = request.GET.get('delivery_type')
    city = request.GET.get('city')
    search_query = request.GET.get('q')

    user_city_name = request.user.customer.city if request.user.is_authenticated and hasattr(request.user, 'customer') and request.user.customer.city else None

    # exclude suppliers with only fast delivery and mismatched cities
    if user_city_name:
        
            user_city = City.objects.get(city=user_city_name)
            suppliers_to_exclude = SupplierProfile.objects.filter(
                supply_details__delivery_service='fast'
            ).exclude(cities_covered=user_city)

            # Exclude suppliers and products
            suppliers = suppliers.exclude(id__in=suppliers_to_exclude.values_list('id', flat=True))
            products = products.exclude(City__suppliers__in=suppliers_to_exclude)

           
            

    # Apply filters
    if category:
        products = products.filter(category=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if delivery_type:
        if delivery_type == 'fast':
            # Filter for fast delivery *and* matching city
            if user_city_name:
                try:
                    user_city = City.objects.get(city=user_city_name)
                    products = products.filter(
                        Q(City__suppliers__supply_details__delivery_service='fast') |
                        Q(City__suppliers__supply_details__delivery_service='both'),
                        City=user_city  # Ensure the product's city matches the user's city
                    )
                except City.DoesNotExist:
                    # Handle the case where the user's city doesn't exist
                    products = Product.objects.none()  # No results if city doesn't exist
            else:
                # If no user city, show no results
                products = Product.objects.none()

        elif delivery_type == 'shipping':
            products = products.filter(
                Q(City__suppliers__supply_details__delivery_service='shipping') |
                Q(City__suppliers__supply_details__delivery_service='both')
            )
        else:
            products = products.filter(City__suppliers__supply_details__delivery_service=delivery_type)

    if city:
        products = products.filter(City__id=city)

    # Apply search *after* filters
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
        suppliers = suppliers.filter(
            Q(user__username__icontains=search_query) | Q(commercial_info__store_name__icontains=search_query)
        )


    # Group products by supplier
    supplier_products = {}
    for product in products:
        for supplier in product.City.suppliers.all():  # Iterate through suppliers
            if supplier not in supplier_products:
                supplier_products[supplier] = []
            supplier_products[supplier].append(product)

    # Prepare context
    context = {
        'suppliers': suppliers,
        'supplier_products': supplier_products,
        'categories': Product.ProductCategory.choices,
        'selected_categories': request.GET.getlist('category'),
        'covered_cities': City.objects.all(),
        'request': request,
        'product_categories': Product.ProductCategory.choices,
    }
    return render(request, 'main/our_suppliers.html', context)