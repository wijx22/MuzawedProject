from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path("cart/",view=views.cart_view,name="cart_view"),
    path("add_to_cart/<product_id>/",view=views.add_to_cart_view,name="add_to_cart_view"),
    path('supplier/orders/', views.supplier_orders_view, name='supplier_orders'),
    path('supplier/orders/<int:order_id>/', views.supplier_order_detail, name='supplier_order_detail'),


]
