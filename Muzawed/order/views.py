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

# def remove_from_cart_view(request: HttpRequest, product_id: int):
#     """Remove a product from the cart."""
#     if not request.user.is_authenticated:
#         messages.error(request, "You must be logged in to manage your cart.", "alert-danger")
#         return redirect("accounts:sign_in")

#     try:
#         with transaction.atomic():
#             product = get_object_or_404(Product, id=product_id)
#             cart = get_object_or_404(Cart, user=request.user)
#             cart_item = get_object_or_404(CartItem, user=request.user, product=product)

#             cart.items.remove(cart_item)
#             cart_item.delete()
#             messages.warning(request, "Product removed from cart.", "alert-warning")

#     except Exception as e:
#         print(e)
#         messages.error(request, "An error occurred while removing the product.", "alert-danger")

#     return redirect("products:cart_view")



# def increase_cart_quantity_view(request: HttpRequest, product_id: int):
#     """Increase the quantity of a product in the cart."""
#     if not request.user.is_authenticated:
#         messages.error(request, "You must be logged in to modify your cart.", "alert-danger")
#         return redirect("accounts:sign_in")
#     try:
#         with transaction.atomic():
#             cart = get_object_or_404(Cart, user=request.user)
#             item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

#             item.quantity += 1
#             item.save()
#             messages.success(request, "Product quantity increased.", "alert-success")

#     except Exception as e:
#         print(e)
#         messages.error(request, "An error occurred while updating quantity.", "alert-danger")

#     return redirect("products:cart_view")



# def decrease_cart_quantity_view(request: HttpRequest, product_id: int):
#     """Reduce the quantity of a product in the cart or delete it if the quantity reaches 1."""
#     if not request.user.is_authenticated:
#         messages.error(request, "You must be logged in to modify your cart.", "alert-danger")
#         return redirect("accounts:sign_in")

#     try:
#         with transaction.atomic():
#             cart = get_object_or_404(Cart, user=request.user)
#             item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

#             if item.quantity > 1:
#                 item.quantity -= 1
#                 item.save()
#                 messages.info(request, "Product quantity decreased.", "alert-info")
#             else:
#                 item.delete()
#                 messages.warning(request, "Product removed from cart.", "alert-warning")

#     except Exception as e:
#         print(e)
#         messages.error(request, "An error occurred while updating quantity.", "alert-danger")

#     return redirect("products:cart_view")




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
