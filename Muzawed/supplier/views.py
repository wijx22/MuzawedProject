from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BranchForm, SupplierForm
from .models import Branch, Supplier


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
