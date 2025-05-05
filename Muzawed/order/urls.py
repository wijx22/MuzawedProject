from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path("cart/",view=views.cart_view,name="cart_view"),
    path("add_to_cart/<product_id>/",view=views.add_to_cart_view,name="add_to_cart_view")
]
