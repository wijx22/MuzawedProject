from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BranchForm, SupplierForm, SupplyRequestForm, CommercialInfoForm
from .models import Branch, Supplier , CommercialInfo, SupplyRequest


@login_required
def supplier_details(request: HttpRequest):
    supplier = Supplier.objects.filter(user=request.user).first()
    if not supplier:
        return redirect("supplier:create_supplier_details")
    branches = Branch.objects.filter(supplier=supplier)
    return render(
        request,
        "supplier/supplier-details.html",
        {"supplier": supplier, "branches": branches},
    )


@login_required
def create_supplier_details(request: HttpRequest):
    if request.method == "POST":
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.user = request.user
            supplier.save()
            messages.success(request, "تم إنشاء المورد بنجاح!")
            return redirect("supplier:supplier_details")

    return render(request, "supplier/create-supplier.html")


@login_required
def branch_create(request):
    supplier = get_object_or_404(Supplier, user=request.user)
    if request.method == "POST":
        form = BranchForm(request.POST)
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
    supplier = get_object_or_404(Supplier, user=request.user)
    if request.method == "POST":
        branch_id = request.POST.get("branch_id")
        if branch_id:
            branch = get_object_or_404(Branch, id=branch_id, supplier=supplier)
            branch.delete()
            messages.success(request, "تم حذف الفرع بنجاح!")
            return redirect("supplier:supplier_details")

    messages.success(request, "غير قادر على حذف الفرع!")
    return redirect("supplier:supplier_details")






def add_commercial_info_view(request):
    supplier = Supplier.objects.filter(user=request.user).first()
    if not supplier:
        return redirect("supplier:create_supplier_details")

    form = CommercialInfoForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        commercial_info = form.save(commit=False)
        commercial_info.supplier = request.user.supplier
        commercial_info.save()
        messages.success(request, 'تم بنجاح إضافة المعلومات التجارية للمورد.')

    return render(request, 'supplier/commercial_info_form.html', {'form': form})


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




def crete_request_view(request: HttpRequest):
    supplier = Supplier.objects.get(user=request.user)
    
    commercial_info = CommercialInfo.objects.filter(supplier=supplier).first()

    if not commercial_info:
        messages.error(request, 'يرجى إضافة معلوماتك التجارية قبل إرسال طلب التوريد.')
        return redirect('supplier:add_commercial_info')
    
        
        
    existing_request = SupplyRequest.objects.filter(commercialInfo=commercial_info, status='pending').first()
    if existing_request:
        messages.error(request, 'لقد قمت بالفعل بإرسال طلب توريد قيد الانتظار.')
        return redirect('supplier:commercial_info_form')  


    if request.method == 'POST':
        form = SupplyRequestForm(request.POST)
        if form.is_valid():
            supply_request = form.save(commit=False)
            supply_request.commercialInfo = commercial_info  
            supply_request.save()
            messages.success(request, 'تم إرسال طلب التوريد بنجاح.')
            return redirect('supplier:commercial_info_form') 
    else:
        form = SupplyRequestForm()

    return render(request, 'supplier/crete_request.html', {'form': form, 'commercial_info': commercial_info})
