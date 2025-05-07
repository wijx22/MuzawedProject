from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from .forms import CitiesForm, CommercialInfoForm
from .models import City, SupplyDetails , CommercialInfo,Day
from accounts.models import SupplierProfile
from products.models import Product
from django.core.paginator import Paginator
#for reports
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from order.models import CartItem
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model


User = get_user_model()










def supplier_details(request: HttpRequest):
    if request.user.is_authenticated:
        try:
            # Check if the user is a supplier
            supplier:SupplierProfile = request.user.supplier
            if supplier.status ==SupplierProfile.RequestStatusChoises.REJECTED or supplier.status ==SupplierProfile.RequestStatusChoises.NO_REQUEST:
                messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
                return redirect("main:index_view")
            supply_details = supplier.supply_details
            if not supply_details.is_today_available():
                messages.warning(request, 'المتجر مغلق اليوم')
                return redirect("main:index_view")
                  

        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء محاولة عرض المعلومات ')
            return redirect("main:index_view")

    return render(
        request,
        "supplier/supplier-details.html",
        {
            "request":supplier,
            "supplier": supply_details,
        },
    )

def cities_view(request:HttpRequest):
    if request.user.is_authenticated:
        try:
            # Check if the user is a supplier
            supplier:SupplierProfile = request.user.supplier
            if supplier.status !=SupplierProfile.RequestStatusChoises.ACCEPTED:
                messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
                return redirect("main:index_view")
            covered_cities = supplier.cities_covered.all()  

            # Get all available city choices
            all_city_choices = City.CityChoices.choices

            # Filter out covered cities
            available_city_choices = [
                (value, display) for value, display in all_city_choices
                if value not in covered_cities.values_list('city', flat=True)
            ]
           

        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء محاولة عرض المعلومات ')
            return redirect("main:index_view")

    return render(
            request,
            "supplier/cities.html",
            {
                "cities": covered_cities,
                "available_city_choices": available_city_choices,  
            },
        )

def add_city_view(request: HttpRequest):
    if request.user.is_authenticated:
        try:
            # Check if the user is a supplier
            supplier = request.user.supplier
            
            if request.method == "POST":
                form = CitiesForm(request.POST)
                if form.is_valid():
                    city:City = form.save(commit=False)  
                    city.save()  
                    city.suppliers.add(supplier) 
                    messages.success(request, "تم إضافة المدينة بنجاح!")
                    return redirect("supplier:cities_view")
                else:
                    messages.error(request, "يرجى التحقق من بيانات المدينة.")


        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء محاولة عرض المعلومات')

    return redirect("main:index_view") 

def delete_city_view(request: HttpRequest, city_id: int):
    
    if request.user.is_authenticated:
        try:
            # Check if the user is a supplier
            supplier:SupplierProfile = request.user.supplier

            # Get the city to be deleted
            city = get_object_or_404(City, id=city_id, suppliers=supplier)

            # Remove the supplier from the city's suppliers
            city.suppliers.remove(supplier)

            # Optionally delete the city if no suppliers are left
            if not city.suppliers.exists():
                city.delete()

            messages.success(request, "تم حذف المدينة بنجاح!")
            return redirect("supplier:cities_view")

        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء محاولة حذف المدينة')

    return redirect("main:index_view")

def update_commercial_data_view(request: HttpRequest):
    if request.user.is_authenticated:
        try:
            # Check if the user is a supplier
            supplier = request.user.supplier
            commercial_info=CommercialInfo.objects.filter(supplier=supplier).first()

            if request.method == 'POST':
                # Pass the instance to the form for updating
                form = CommercialInfoForm(request.POST, request.FILES, instance=commercial_info)

                if form.is_valid():
                    commercial_info = form.save(commit=False) 
                    commercial_info.supplier = supplier 
                    commercial_info.save() 
                    messages.success(request, 'تم بنجاح تحديث المعلومات التجارية .')
                    return redirect("supplier:store_info_view")
                else:
                    messages.error(request, 'الرجاء تصحيح الأخطاء في النموذج.')

            else:
                form = CommercialInfoForm(instance=commercial_info)

            return render(request, 'supplier/update_commercial_info.html', {'form': form ,"commercial_info":commercial_info})

        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء محاولة تحديث المعلومات التجارية يرجى المحاولة مرة اخرى ')
            return redirect("main:store_info_view")

    return redirect("accounts:sign_in")


def update_supply_details_view(request: HttpRequest):
    if request.user.is_authenticated:
        try:
            # Check if the user is a supplier
            supplier = request.user.supplier
            supply_details = SupplyDetails.objects.filter(supplier=supplier).first()

            if request.method == 'POST':
                if supply_details:
                    # Extract data from request
                    late_payment_options = request.POST.get('late_payment_options')
                    fast_service_details = request.POST.get('fast_service_details')
                    order_lead_time_days = request.POST.get('order_lead_time_days')
                    delivery_service = request.POST.get('delivery_service')
                    supply_sector = request.POST.get('supply_sector')
                    # Handle the image upload
                    logo = request.FILES.get('logo')

                    # Clear fast_service_details if delivery_service is not 'fast' or 'both'
                    if delivery_service != 'fast' and delivery_service != 'both':
                        supply_details.fast_service_details = None  # Or '' if it's a CharField

                    else:
                        supply_details.fast_service_details = fast_service_details


                    # Clear fast_service_details if delivery_service is not 'fast' or 'both'
                    if delivery_service != 'shipping' and delivery_service != 'both':
                        supply_details.order_lead_time_days = None  # Or '' if it's a CharField

                    else:
                        supply_details.order_lead_time_days = order_lead_time_days
                    print(delivery_service)
                    # Update the existing SupplyDetails instance
                    supply_details.supply_sector = supply_sector
                    supply_details.delivery_service = delivery_service
                    supply_details.late_payment_options = late_payment_options is not None  # Correctly handle the boolean
                    if logo:
                        supply_details.logo = logo  # Update the logo only if a new one is uploaded

                    # Save the updated SupplyDetails to the database
                    supply_details.save()

                    # Handle the supply_days separately (assuming it's a ManyToManyField)
                    selected_day_ids = request.POST.getlist('supply_days')
                    day_objects = Day.objects.filter(id__in=selected_day_ids)  # Or pk__in if you use pk
                    supply_details.supply_days.set(day_objects)

                    # Show success message
                    messages.success(request, 'تم تحديث معلومات التوريد بنجاح')
                    return redirect("supplier:store_info_view")
                else:
                    messages.error(request, 'معلومات التوريد غير موجودة.')  # Handle the case where supply_details doesn't exist
                    return redirect("supplier:store_info_view")

            supply_sector_choices = SupplyDetails._meta.get_field('supply_sector').choices
            delivery_service_choices = SupplyDetails._meta.get_field('delivery_service').choices
            days = Day.objects.all()

            return render(request, "supplier/update_supply_details.html", {
                "supply_details": supply_details,
                "supply_sector_choices": supply_sector_choices,
                "delivery_service_choices": delivery_service_choices,
                "days": days,
            })

        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء محاولة تحديث معلومات التوريد يرجى المحاولة مرة اخرى ')
            return redirect("main:index_view")

    return redirect("accounts:sign_in")






def supply_request_view(request: HttpRequest):
    if request.user.is_authenticated:
        try:
            supplier:SupplierProfile = request.user.supplier

            if supplier.status ==SupplierProfile.RequestStatusChoises.REJECTED or supplier.status ==SupplierProfile.RequestStatusChoises.NO_REQUEST:

                commercial_info = CommercialInfo.objects.filter(supplier=supplier).first()
                supply_details = SupplyDetails.objects.filter(supplier=supplier).first()

                if request.method == 'POST':
                    with transaction.atomic():  
                        # Handle commercial info form
                        commercial_form = CommercialInfoForm(request.POST or None, request.FILES or None, instance=commercial_info)

                        if commercial_form.is_valid():
                            if commercial_info:
                                commercial_info.delete()
                            commercial_info = commercial_form.save(commit=False)
                            commercial_info.supplier = supplier
                            commercial_info.save()

                        # Handle supply details form
                        selected_days = request.POST.getlist('supply_days')
                        late_payment_options = request.POST.get('late_payment_options')
                        fast_service_details = request.POST.get('fast_service_details')
                        order_lead_time_days = request.POST.get('order_lead_time_days')
                        delivery_service = request.POST.get('delivery_service')
                        supply_sector = request.POST.get('supply_sector')
                        logo = request.FILES.get('logo')
                        if not fast_service_details:
                            fast_service_details = None  

                        if not order_lead_time_days:
                            order_lead_time_days = None 
                        if supply_details:
                            supply_details.delete()

                        # Create and save the new SupplyDetails instance
                        supply_details = SupplyDetails(
                            supplier=supplier,
                            logo=logo,
                            supply_sector=supply_sector,
                            delivery_service=delivery_service,
                            order_lead_time_days=order_lead_time_days,
                            fast_service_details=fast_service_details,
                            late_payment_options=late_payment_options is not None,
                        )
                        supply_details.save()

                        day_objects = Day.objects.filter(pk__in=selected_days)
                        supply_details.supply_days.set(day_objects)

                        # Update supplier status
                        supplier.status = SupplierProfile.RequestStatusChoises.PENDING
                        supplier.save()

                        messages.success(request, 'تم بنجاح إضافة المعلومات التجارية ومعلومات التوريد.')
                        return redirect("supplier:supplier_details")

                # Supply sector choices 
                days=Day.objects.all()
                supply_sector_choices = SupplyDetails._meta.get_field('supply_sector').choices
                delivery_service_choices = SupplyDetails._meta.get_field('delivery_service').choices
                commercial_form = CommercialInfoForm(instance=commercial_info) 

                return render(request, "supplier/supply_request.html", {
                    "days":days,
                    'commercial_form': commercial_form,
                    'supply_sector_choices': supply_sector_choices,
                    'delivery_service_choices': delivery_service_choices,
                })
            else:
                messages.warning(request, 'عذرًا لديك طلب توريد ساري ')
                return redirect("main:index_view")


        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء معالجة البيانات.')
            return redirect("main:index_view")

    return redirect("accounts:sign_in")


def store_info_view(request:HttpRequest):
    if request.user.is_authenticated:
        try:
            supplier:SupplierProfile = request.user.supplier

            if supplier.status ==SupplierProfile.RequestStatusChoises.ACCEPTED :

                commercial_info = CommercialInfo.objects.filter(supplier=supplier).first()
                supply_details = SupplyDetails.objects.filter(supplier=supplier).first()

                return render(request, "supplier/store_information.html", {
                    "commercial_info":commercial_info,
                    "supply_details": supply_details,
                })
            else:
                messages.error(request, "حسابك قيد المراجعة من قبل الإدارة. سيتم تفعيله قريبًا.")
                return redirect('main:index_view') 
             

        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء معالجة البيانات.')
            return redirect("main:index_view")

    return redirect("accounts:sign_in")


def store_view(request: HttpRequest ):

    supplier: SupplierProfile = SupplierProfile.objects.get(pk= request.GET.get('supplier_id'))
    commercial_info = CommercialInfo.objects.filter(supplier=supplier).first()
    supply_details = SupplyDetails.objects.filter(supplier=supplier).first()
    # products = Product.objects.all()
    products = Product.objects.filter( City__suppliers=supplier)

    covered_cities = supplier.cities_covered.all()

    # Get filter parameters from the request
    selected_categories = request.GET.getlist('category')  
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    city = request.GET.get('city')

    # Apply filters
    if selected_categories:
        products = products.filter(category__in=selected_categories)  # Filter by category (using __in for multiple values)
    if min_price:
        products = products.filter(price__gte=min_price)  # Filter by minimum price (greater than or equal to)
    if max_price:
        products = products.filter(price__lte=max_price)  # Filter by maximum price (less than or equal to)
    if city:
        products = products.filter(City=city)  # Filter by city

    categories = Product.ProductCategory.choices

    page_number = request.GET.get("page", 1)

    paginator = Paginator(products, 4)
    store_page = paginator.get_page(page_number)
    return render(
        request,
        "supplier/store.html",
        {
            "commercial_info": commercial_info,
            "categories": categories,
            "supply_details": supply_details,
            "products": store_page,
            "covered_cities": covered_cities,
            "selected_categories": selected_categories,
            "get_params": request.GET  # Pass the GET parameters to the template
        },
    )
    # return render(
    #     request,
    #     "supplier/store.html",
    #     {
    #         "commercial_info": commercial_info,
    #         "categories": categories,
    #         "supply_details": supply_details,
    #         "products": store_page,
    #         "covered_cities": covered_cities,
    #         "selected_categories": selected_categories,  
    #     },
    # )
    
    
    
    


 
 
# Dashboard for reports waiting for finish products (should have a user or supplier for each product)
# This is a placeholder for the dashboard view   
@login_required
def supplier_reports_dashboard(request):
    # Overview page with links or charts
    return render(request, "supplier/reports/dashboard.html")





@login_required
def report_revenue_by_product(request):
    
    # Ensure user is authenticated 
    # if  hasattr(request.user, 'staff'):
    #     return HttpResponseForbidden("هذه الصفحة مخصصة للموردين فقط.")

    # # Fetch supplier's products
    # supplier_products = Product.objects.filter(supplier=SupplierProfile)

    # # Calculate revenue per product for completed orders
    # revenue_data = (
    #     CartItem.objects
    #     .filter(product__in=supplier_products, order__status='closed')
    #     .values('product__name')
    #     .annotate(
    #         total_quantity=Sum('quantity'),
    #         total_revenue=Sum(F('quantity') * F('unit_price'))
    #     )
    #     .order_by('-total_revenue')
    # )

    # context = {
    #     "data": revenue_data
    # }
    return render(request, "supplier/reports/revenue.html")




@login_required
def report_user_behavior(request):
    # Analyze customer behavior
    context = {
        "data": []  # Placeholder for unique users and order frequency
    }
    return render(request, "supplier/reports/user_behavior.html", context)




@login_required
def report_product_performance(request):
    # Evaluate performance and low-performing products
    context = {
        "data": []  # Placeholder for product stats, ratings
    }
    return render(request, "supplier/reports/product_performance.html", context)

