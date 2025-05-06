from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order
from django.http import HttpRequest
from django.urls import reverse
# Create your views here.
from .models import Product
from .models import Order, CartItem
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from accounts.models import ProfileBeneficiary, SupplierProfile
# def cart_view(request:HttpRequest):
#     items =Product.objects.all()
#     return render(request, "order/cart.html",{"items":items})


def cart_view(request: HttpRequest, order_id: int):
    """Display the contents of the cart to the user."""
    if not request.user.is_authenticated:
        messages.error(request, "يجب عليك تسجيل الدخول لعرض سلة التسوق الخاصة بك.", "alert-danger")
        return redirect("accounts:sign_in")

    cart = get_object_or_404(Order, id=order_id)
    items = cart.items.all()
    return render(request, "order/cart.html", {"items": items})

def add_to_cart_view(request: HttpRequest, product_id: int):
    supplier_id = request.GET.get('supplier_id')
    print("this is the error ")
    print(request.GET)
    if not supplier_id:
        messages.error(request, "try", "alert-danger")
        return redirect("main:index_view")

    try:
        supplier_id = int(supplier_id)
    except ValueError as error:
        messages.error(request, "المورد غير موجود.", "alert-danger")
        print("an error ",error)
        return redirect("main:index_view")

    try:
        supplier = SupplierProfile.objects.get(pk=supplier_id)

    except SupplierProfile.DoesNotExist as error:
        messages.error(request, "المورد غير موجود.", "alert-danger")
        print("an error ",error)

        return redirect("main:index_view")

    cart = Order.objects.filter(supplier=supplier, beneficiary=request.user, in_cart=True).first()
    if cart is None:
        cart = Order(supplier=supplier, beneficiary=request.user)
        cart.save()

    """Add a product to the cart, and increase the quantity if it already exists."""
    if not request.user.is_authenticated:
        messages.error(request, "يجب عليك تسجيل الدخول لإضافة عناصر إلى سلة التسوق الخاصة بك.", "alert-danger")
        return redirect("accounts:sign_in")

    if not ProfileBeneficiary.objects.filter(user=request.user).exists():
        messages.error(request, "يمكن للمستخدم فقط إضافة عناصر إلى سلة التسوق.", "alert-danger")
        return redirect('main:index_view')

    try:
        with transaction.atomic():
            product = get_object_or_404(Product, id=product_id)
            if product.stock == 0:
                messages.warning(request, "عذرًا، هذا المنتج غير متوفر حاليًا.", "alert-warning")
                return redirect(reverse("products:product_details_view", kwargs={'product_id': product_id}) + f"?supplier_id={supplier_id}")

            quantity = int(request.GET.get('quantity', product.min_order_quantity))
            if quantity <= 0:
                messages.error(request, "الكمية غير صالحة.", "alert-danger")
                return redirect(reverse("products:product_details_view", kwargs={'product_id': product_id}) + f"?supplier_id={supplier_id}")

            # Try to get the existing cart item
            cart_item = CartItem.objects.filter(order=cart, product=product).first()
            if cart_item:
                # If the item exists, update the quantity
                cart_item.quantity = F('quantity') + quantity
                cart_item.save()  # The save() method now handles subtotal calculation
            else:
                # If the item doesn't exist, create a new one
                unit_price = product.price
                cart_item = CartItem(order=cart, product=product, quantity=quantity, unit_price=unit_price)
                cart_item.save() 
     

            messages.success(request, "تمت إضافة المنتج إلى العربة بنجاح", "alert-success")

    except Exception as e:
        print(e)
        messages.error(request, f"حدث خطأ أثناء إضافة المنتج: {e}", "alert-danger")

    return redirect(reverse("products:product_details_view", kwargs={'product_id': product_id}) + f"?supplier_id={supplier_id}")



def cart_orders_view(request):
    """
    Displays all 'in cart' orders for the logged-in user as cards,
    with options to view details/checkout or delete the order.
    """
    if not request.user.is_authenticated:
        return render(request, 'accounts/sign_in.html')  

    cart_orders = Order.objects.filter(beneficiary=request.user, in_cart=True).order_by('created_at')

    context = {
        'cart_orders': cart_orders,
    }
    return render(request, 'order/cart_orders.html',context)


def delete_cart_order_view(request, order_id):
    """
    Deletes an entire order from the cart.
    """

    order = get_object_or_404(Order, id=order_id, beneficiary=request.user, in_cart=True)
    order.delete()  # This will also delete associated CartItems due to on_delete=CASCADE
    return redirect('order:cart_orders_view')  # Redirect back to the cart view



def supplier_orders_view(request):
    '''Displays all orders related to the current supplier.'''
    supplier: SupplierProfile = request.user.supplier
    orders = Order.objects.filter(supplier=supplier)


    return render(request, 'order/supplier_orders_list.html', {
        'orders': orders
    })



#def supplier_order_detail(request, order_id):
#    '''Shows the details of a specific order for the supplier and allows them to accept or reject the order via POST.'''
#    order = Order.objects.get(id=order_id)
#    if request.method == "POST":
#        action = request.POST.get("action")
#        if action == "accept":
#            order.status = 'processing'  
#            order.save()
#            messages.success(request, "تم قبول الطلب وهو الآن قيد المعالجة.")
#        elif action == "reject":
#            order.status = 'cancelled'  
#            order.save()
#            messages.warning(request, "تم رفض الطلب.")
#            
#        elif action == "set_delivery_date":
#          order.delivery_date = timezone.now()
#          order.save()
#          messages.success(request, "تم تسجيل وقت التوصيل.")
#
#        return redirect('order:supplier_order_detail', order_id=order.id)
#
#    cart_items = order.items.all()
#    return render(request, 'order/supplier_order_detail.html', {
#        'order': order,
#        'cart_items': cart_items
#    })


def supplier_order_detail(request, order_id):
    '''Shows the details of a specific order for the supplier and allows them to accept, reject, delete, or mark as delivered.'''
    order = Order.objects.get(id=order_id)

    # Check if order is already in "processing" or "closed" state
    actions_disabled = order.status in ['processing', 'closed', 'cancelled']
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "accept" and order.status == 'open':
            order.status = 'processing'  
            order.save()
            messages.success(request, "تم قبول الطلب وهو الآن قيد المعالجة.")
        
        elif action == "reject" and order.status == 'open':
            order.status = 'cancelled'  
            order.save()
            messages.warning(request, "تم رفض الطلب.")
        
        elif action == "delete" and not actions_disabled:
            order.delete()
            messages.success(request, "تم حذف الطلب.")
            return redirect('order:supplier_orders')  
        
        elif action == "mark_delivered" and order.status == 'processing':  
            order.status = 'closed'  
            order.delivery_date = timezone.now()  
            order.save()
            messages.success(request, "تم تسليم الطلب بنجاح.")
        
        return redirect('order:supplier_order_detail', order_id=order.id)

    cart_items = order.items.all()
    return render(request, 'order/supplier_order_detail.html', {
        'order': order,
        'cart_items': cart_items,
        'actions_disabled': actions_disabled
    })
