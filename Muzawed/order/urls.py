from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path("cart/<order_id>/",view=views.cart_view,name="cart_view"),
    path('cart/', views.cart_orders_view, name='cart_orders_view'),
    path('my_orders/', views.beneficiary_orders_view, name='beneficiary_orders_view'),
    path('cart/delete/<int:order_id>/', views.delete_cart_order_view, name='delete_cart_order_view'),
    path("add_to_cart/<product_id>/",view=views.add_to_cart_view,name="add_to_cart_view"),
    path('supplier/orders/', views.supplier_orders_view, name='supplier_orders'),
    path('supplier/orders/<int:order_id>/', views.supplier_order_detail, name='supplier_order_detail'),
    path('process_order/<order_id>', views.process_order, name='process_order'),  
]
