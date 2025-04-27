from django.urls import path

from . import views

app_name = "supplier"

urlpatterns = [
    path("supplier-details/", views.supplier_details, name="supplier_details"),
    path(
        "create-supplier/",
        views.create_supplier_details,
        name="create_supplier_details",
    ),
]
