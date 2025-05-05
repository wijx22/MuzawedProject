from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order
from django.http import HttpRequest
# Create your views here.
from .models import Product
from .models import Order, CartItem
from django.utils import timezone
from accounts.models import SupplierProfile



def cart_view(request:HttpRequest):
    items =Product.objects.all()
    return render(request, "order/cart.html",{"items":items})




def add_product_item_view(request:HttpRequest):
    pass




def supplier_orders_view(request):
    supplier: SupplierProfile = request.user.supplier
    orders = Order.objects.filter(supplier=supplier, in_cart=False)


    return render(request, 'order/supplier_orders_list.html', {
        'orders': orders
    })



def supplier_order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.supplier != request.user.supplierprofile:
        messages.error(request, "غير مسموح لك بعرض هذا الطلب.")
        return redirect('supplier_orders_view')  

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "accept":
            order.status = 'processing'  
            order.save()
            messages.success(request, "تم قبول الطلب وهو الآن قيد المعالجة.")
        elif action == "reject":
            order.status = 'cancelled'  
            order.save()
            messages.warning(request, "تم رفض الطلب.")
        return redirect('supplier_order_detail', order_id=order.id)

    cart_items = order.items.all()
    return render(request, 'order/supplier_order_detail.html', {
        'order': order,
        'cart_items': cart_items
    })
