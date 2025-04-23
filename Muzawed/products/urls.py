from django.urls import path
from . import views 

app_name = 'products'

urlpatterns = [
    path("add_product/",view=views.add_product_view, name="add_product_view"),
]
