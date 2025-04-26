from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from .models import Supplier


@login_required
def supplier_details(request: HttpRequest):
    supplier = get_object_or_404(Supplier, user=request.user)
    return render(request, "supplier/supplier-details.html", {"supplier": supplier})
