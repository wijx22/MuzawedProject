from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order
from django.http import HttpRequest
from django.urls import reverse
# Create your views here.
from .models import Product
from .models import Order, CartItem
from django.utils import timezone
from django.contrib import messages
from django.db import transaction

from accounts.models import ProfileBeneficiary, SupplierProfile
def cart_view(request:HttpRequest):
    items =Product.objects.all()
    return render(request, "order/cart.html",{"items":items})





def cart_view(request: HttpRequest, order_id ):
    """Display the contents of the cart to the user."""
    if not request.user.is_authenticated :
        messages.error(request, "You must be logged in to view your cart.", "alert-danger")
        return redirect("accounts:sign_in")
    # if not Profile_User.objects.filter(user=request.user).exists():
    #       messages.error(request, "Only User can view cart.", "alert-danger")
    #       return redirect('main:index_view')

    cart= Order.objects.get(id=order_id)
    return render(request, "cart/cart_view.html", {"cart": cart})


def add_to_cart_view(request: HttpRequest, product_id: int):
    supplier_id = request.GET.get('supplier_id')
    if not supplier_id:
        messages.error(request, "Supplier ID is required.", "alert-danger")
        return redirect("main:index_view")  # Or wherever appropriate

    try:
        supplier_id = int(supplier_id)  # Convert to integer
    except ValueError:
        messages.error(request, "Invalid Supplier ID.", "alert-danger")
        return redirect("main:index_view")  # Or wherever appropriate

    try:
        supplier = SupplierProfile.objects.get(pk=supplier_id)  # Get the Supplier object
    except SupplierProfile.DoesNotExist:
        messages.error(request, "Supplier not found.", "alert-danger")
        return redirect("main:index_view")  # Or wherever appropriate

    cart = Order.objects.filter(supplier=supplier, beneficiary=request.user, in_cart=True).first()
    if cart is None:  # Check if cart is None
        cart = Order(supplier=supplier, beneficiary=request.user)
        cart.save()

    """Add a product to the cart, and increase the quantity if it already exists."""
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add items to your cart.", "alert-danger")
        return redirect("accounts:sign_in")

    if not ProfileBeneficiary.objects.filter(user=request.user).exists():
        messages.error(request, "Only User can add to cart.", "alert-danger")
        return redirect('main:index_view')

    try:
        with transaction.atomic():
            product = get_object_or_404(Product, id=product_id)
            if product.stock == 0:
                messages.warning(request, "Sorry, this product is currently out of stock.", "alert-warning")
                return redirect("products:product_details_view", product_id=product.id, supplier_id=supplier_id)  # Pass supplier_id on redirect

            quantity = int(request.GET.get('quantity', 1))
            if quantity <= 0:
                messages.error(request, "Invalid quantity.", "alert-danger")
                return redirect("products:product_details_view", product_id=product.id, supplier_id=supplier_id) # Pass supplier_id on redirect

            unit_price = product.price
            cart_item = CartItem(order=cart, product=product, quantity=quantity, unit_price=unit_price)
            cart_item.save()

            messages.success(request, "تم اضافة المنتج الى العربة بنجاح", "alert-success")

    except Exception as e:
        print(e)
        messages.error(request, f"An error occurred while adding the product: {e}", "alert-danger")

    return redirect(reverse("products:product_details_view", kwargs={'product_id': product_id}) + f"?supplier_id={supplier_id}") # Pass supplier_id on redirect





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
