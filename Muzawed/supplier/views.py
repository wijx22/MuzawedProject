from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CitiesForm, SupplyRequestForm, CommercialInfoForm
from .models import City, SupplyDetails , CommercialInfo
from accounts.models import SupplierProfile

@login_required
def supplier_details(request: HttpRequest):
    if request.user.is_authenticated:
        try:
            # Check if the user is a supplier
            supplier = request.user.supplier
            commercial_info=supplier.commercial_info
            supply_details=supplier.supply_details
            cities=City.objects.filter(suppliers=supplier)           
        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء محاولة اضافة المعلومات التجارية يرجى المحاولة مرة اخرى ')
            return redirect("main:supplie_view")  

    return render(
        request,
        "supplier/supplier-details.html",
        {"supplier": supplier, "branches": cities},
    )


@login_required
def branch_create(request:HttpRequest):
    supplier = get_object_or_404(SupplyDetails, user=request.user)
    if request.method == "POST":
        form = CitiesForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.supplier = supplier
            branch.save()
            messages.success(request, "تم إنشاء الفرع بنجاح!")
            return redirect("supplier:supplier_details")
    else:
        messages.error(request, "غير قادر على إنشاء الفرع!")
        return redirect("supplier:supplier_details")


@login_required
def branch_delete(request):
    supplier = get_object_or_404(SupplyDetails, user=request.user)
    if request.method == "POST":
        branch_id = request.POST.get("branch_id")
        if branch_id:
            branch = get_object_or_404(City, id=branch_id, supplier=supplier)
            branch.delete()
            messages.success(request, "تم حذف الفرع بنجاح!")
            return redirect("supplier:supplier_details")

    messages.success(request, "غير قادر على حذف الفرع!")
    return redirect("supplier:supplier_details")

def update_commercial_info_view(request):
    supplier = Supplier.objects.filter(user=request.user).first()
    if not supplier:
        return redirect("supplier:create_supplier_details")

    commercial_info = supplier.commercialinfo_set.first()
    if not commercial_info:
        return redirect('supplier:add_commercial_info')

    form = CommercialInfoForm(request.POST or None, request.FILES or None, instance=commercial_info)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'تم تحديث المعلومات التجارية بنجاح.')
        return redirect('supplier:dashboard')  

    return render(request, 'supplier/commercial_info_form.html', {'form': form})


#done
def commercial_data_view(request: HttpRequest):
    if request.user.is_authenticated:
        try:
            # Check if the user is a supplier
            supplier = request.user.supplier
            form = CommercialInfoForm(request.POST or None, request.FILES or None)
            commercial_info=CommercialInfo.objects.filter(supplier=supplier).first()
            print("innn")
            print(commercial_info)
            if request.method == 'POST':
                if commercial_info:
                    
                    commercial_info.delete()

                if form.is_valid():
                    commercial_info = form.save(commit=False)
                    commercial_info.supplier = supplier
                    commercial_info.save()
                    messages.success(request, 'تم بنجاح إضافة المعلومات التجارية للمورد.')
                    return redirect("supplier:supply_details_view")

            return render(request, 'supplier/commercial_info_form.html', {'form': form})

        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء محاولة اضافة المعلومات التجارية يرجى المحاولة مرة اخرى ')
            return redirect("main:supplie_view")

    return redirect("accounts:sign_in")          

def supply_details_view(request: HttpRequest):
    if request.user.is_authenticated:
        try:
            # Check if the user is a supplier
            supplier = request.user.supplier
            supply_details=SupplyDetails.objects.filter(supplier=supplier).first()
            print(type(supply_details))
            print("in details")
            if request.method == 'POST':
                if supply_details:
                    
                    supply_details.delete()


                # Extract data from request
                supply_days = request.POST.get('supply_days')
                late_payment_options = request.POST.get('late_payment_options')
                fast_service_details = request.POST.get('fast_service_details')
                order_lead_time_days = request.POST.get('order_lead_time_days')
                delivery_service = request.POST.get('delivery_service')
                supply_sector = request.POST.get('supply_sector')

                # Handle the image upload
                logo = request.FILES.get('logo')

                # Create a new Product instance
                supplyDetails = SupplyDetails(
                    supplier=supplier,
                    logo=logo,
                    supply_sector=supply_sector,
                    delivery_service=delivery_service,
                    order_lead_time_days=order_lead_time_days,
                    fast_service_details=fast_service_details,
                    late_payment_options=late_payment_options is not None,
                    supply_days=supply_days,
                )

                # Save the product to the database
                supplyDetails.save()

                # Show success message
                messages.success(request, 'تم اضافة معلومات التوريد بنجاح')
                supplier.status = SupplierProfile.RequestStatusChoises.PENDING
                supplier.save() 
                return redirect("supplier:supplier_details")

            return render(request, "supplier/create-supplier.html")


        except AttributeError:
            messages.warning(request, 'انت غير مصرح للوصول الى هذه الصفحة')
            return redirect("main:index_view")

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء محاولة اضافة معلومات التوريد يرجى المحاولة مرة اخرى ')
            return redirect("main:supplie_view")

    return redirect("accounts:sign_in")          




def create_supply_request(request: HttpRequest):
    #4 option 
    #1 no request back end + front
    # pending handeled in front end 
    #3 rejected back end + front
    #4 accepted handled in front end

    if request.user.is_authenticated:
        try:
            supplier=request.user.supplier
            
            commercial_info=supplier.commercial_info
            supply_details=supplier.supply_details
            
            print(commercial_info)
            print(supply_details)



        except AttributeError:
            return redirect('supplier:commercial_data_view')

        except Exception as error:
            print("An error occurred:", error)
            messages.error(request, 'حدث خطأ اثناء محاولة اضافة معلومات التوريد يرجى المحاولة مرة اخرى ')
            return redirect("main:supplie_view")
        return redirect("main:supplie_view")

    