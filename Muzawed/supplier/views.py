from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SupplierForm
from .models import Supplier


@login_required
def supplier_details(request: HttpRequest):
    supplier = Supplier.objects.filter(user=request.user).first()
    if not supplier:
        return redirect("supplier:create_supplier_details")
    return render(request, "supplier/supplier-details.html", {"supplier": supplier})


@login_required
def create_supplier_details(request: HttpRequest):
    if request.method == "POST":
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.user = request.user
            supplier.save()
            messages.success(request, "Supplier created successfully!")
            return redirect("supplier:supplier_details")

    return render(request, "supplier/create-supplier.html")
