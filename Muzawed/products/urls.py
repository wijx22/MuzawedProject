from django.urls import path
from . import views 

app_name = 'products'

urlpatterns = [
    path("add_product/",view=views.add_product_view, name="add_product_view"),
    path("remove_product/<product_id>",view=views.remove_product_view, name="remove_product_view"),
    path("update_product/<product_id>",view=views.update_product_view, name="update_product_view"),
    path("product_stock/",view=views.stock_view, name="stock_view"),
    path("product_details/<product_id>",view=views.product_details_view, name="product_details_view"),
    path("",view=views.products_view, name="products_view"),
]
