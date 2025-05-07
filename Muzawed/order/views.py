from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from notification.models import Notification 
from payment.models import Payment
from django.http import HttpRequest
from django.urls import reverse
from .models import Product
from .models import Order, CartItem
from django.db import transaction
from django.db.models import F
from accounts.models import ProfileBeneficiary, SupplierProfile
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from payment.models import Payment  


def cart_view(request: HttpRequest, order_id: int):
    """Display the contents of the cart to the user."""
    if not request.user.is_authenticated:
        messages.error(request, "يجب عليك تسجيل الدخول لعرض سلة التسوق الخاصة بك.", "alert-danger")
        return redirect("accounts:sign_in")

    cart = get_object_or_404(Order, id=order_id)
    items = cart.items.all()

    if not items:  # Check if the cart is empty
        cart.delete()
        messages.info(request, "سلة التسوق الخاصة بالطلب اصبحت فارغة.", "alert-info")  
        return redirect("order:cart_orders_view") 

    return render(request, "order/cart.html", {"order": cart, "items": items})

def add_to_cart_view(request: HttpRequest, product_id: int):
    if not request.user.is_authenticated:
        messages.error(request, "يجب عليك تسجيل الدخول لاضافة منتجات لسلة التسوق الخاصة بك.", "alert-danger")
        return redirect("accounts:sign_in")
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

    return redirect(reverse("supplier:store_view") + f"?supplier_id={supplier_id}")


def remove_from_cart_view(request:HttpRequest ,order_id, cartItem_id):
    try:

        item = get_object_or_404(CartItem, id=cartItem_id)
        item.delete()  
        

    except Exception as error :
        messages.error(request, f"حدث خطأ أثناء حذف المنتج", "alert-danger")
    return redirect("order:cart_view", order_id)

        

def cart_orders_view(request):
    """
    Displays all 'in cart' orders for the logged-in user as cards,
    with options to view details/checkout or delete the order.
    """
    if not request.user.is_authenticated:
        messages.error(request, "يجب عليك تسجيل الدخول لعرض سلة التسوق الخاصة بك.", "alert-danger")
        return redirect("accounts:sign_in")


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
    order.delete()  
    messages.success(request, "تم حذف الطلب بنجاح!")

    return redirect('order:cart_orders_view')  



def supplier_orders_view(request):
    '''Displays all orders related to the current supplier.'''
      
    if not request.user.is_authenticated:
       messages.error(request, "يجب عليك تسجيل الدخول للوصول إلى هذه الصفحة.", "alert-danger")
       return redirect("accounts:sign_in")

    if not SupplierProfile.objects.filter(user=request.user).exists():
        messages.error(request, "هذه الصفحة مخصصة لحسابات الموردين فقط.", "alert-danger")
        return redirect('main:index_view')


    supplier: SupplierProfile = request.user.supplier
    orders = Order.objects.filter(supplier=supplier)

    order_status = request.GET.get('status')  

    if order_status:
        orders = orders.filter(status=order_status)  

    return render(request, 'order/supplier_orders_list.html', {
        'orders': orders
    })


def process_order(request, order_id):
    if not request.user.is_authenticated:
        messages.error(request, "يجب عليك تسجيل الدخول لاتمام الطلب.", "alert-danger")
        return redirect("accounts:sign_in")

    try:
        order = get_object_or_404(Order, pk=order_id)

        if request.method == 'POST':
            payment_method = request.POST.get('payment_method')
            cart_items = order.items.all()
            total_amount = order.total

            out_of_stock_items = []
            for item in cart_items:
                if item.product.stock < item.quantity:
                    out_of_stock_items.append(item.product.name)

            if out_of_stock_items:
                error_message = " المنتجات التالية غير متوفرة بالكمية المطلوبة يرجى حذفها لاتمام الطلب: " + ", ".join(out_of_stock_items)
                messages.error(request, error_message)
                return redirect('order:cart_view', order.id)

            # Create Payment object with PENDING status
            payment = Payment(
                order=order,
                payment_method=payment_method,
                total_amount=total_amount,
                status=Payment.StatusChoices.PENDING  # Use the enum
            )
            payment.save()

            if payment_method == 'credit':
                # Redirect to payment gateway with payment ID
             
                return redirect( reverse('payment:payment_gateway', kwargs={'payment_id': payment.id}) )
            else:
                # For cash or deferred, complete the order immediately
                complete_order(order, cart_items, payment)
                messages.success(request, "تم اتمام الطلب بنجاح!")
                return redirect('order:cart_orders_view')

    except Exception as error:
        messages.error(request, "حدث خطأ اثناء محاولة الوصول للعربة")
        print(error)
        return redirect('order:cart_orders_view')

    return render(request, 'order/cart_orders.html')



def complete_order(order, cart_items, payment):
    """Completes the order process: reduces stock, marks order as complete."""
    for item in cart_items:
        product = item.product
        product.stock -= item.quantity
        product.save()

    order.in_cart = False
    order.save()

def supplier_order_detail(request, order_id):
    '''Shows the details of a specific order for the supplier and allows them to accept, reject, delete, or mark as delivered.'''

    if not request.user.is_authenticated:
        messages.error(request, "يجب عليك تسجيل الدخول للوصول إلى هذه الصفحة.", "alert-danger")
        return redirect("accounts:sign_in")

    if not SupplierProfile.objects.filter(user=request.user).exists():
        messages.error(request, "هذه الصفحة مخصصة لحسابات الموردين فقط.", "alert-danger")
        return redirect('main:index_view')

    order = Order.objects.get(id=order_id)

    # Check if order is already in "processing" or "closed" state
    actions_disabled = order.status in ['processing', 'closed', 'cancelled']
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "accept" and order.status == 'open':
            order.status = 'processing'  
            order.save()
            messages.success(request, "تم قبول الطلب وهو الآن قيد المعالجة.")

            Notification.objects.create(
                recipient=order.beneficiary,  # المستفيد
                notification_type='alert',
                message='تم قبول طلبك وهو الآن قيد المعالجة.'
            )

        
        elif action == "reject" and order.status == 'open':
            order.status = 'cancelled'  
            order.save()
            messages.warning(request, "تم رفض الطلب.")

            Notification.objects.create(
                recipient=order.beneficiary,
                notification_type='alert',
                message=' تم رفض طلبك من قبل المورد .'
            )

        
        elif action == "delete" and not actions_disabled:
            order.delete()
            messages.success(request, "تم حذف الطلب.")
            return redirect('order:supplier_orders')  
        
        elif action == "mark_delivered" and order.status == 'processing':  
            order.status = 'closed'  
            order.delivery_date = timezone.now()  
            order.save()
            messages.success(request, "تم تسليم الطلب بنجاح.")

            Notification.objects.create(
                recipient=order.beneficiary,
                notification_type='alert',
                message='تم تسليم طلبك بنجاح.'
            )

        
        return redirect('order:supplier_order_detail', order_id=order.id)

    cart_items = order.items.all()
    return render(request, 'order/supplier_order_detail.html', {
        'order': order,
        'cart_items': cart_items,
        'actions_disabled': actions_disabled
    })

def beneficiary_orders_view(request):
    open_or_processing_orders = Order.objects.filter(status__in=['open', 'processing'],beneficiary=request.user)
    cancelled_or_rejected_orders = Order.objects.filter(status__in=['cancelled', 'closed'],beneficiary=request.user)

    context = {
        'current_orders': open_or_processing_orders,
        'closed_orders': cancelled_or_rejected_orders,
    }
    return render(request, 'order/orders.html', context)