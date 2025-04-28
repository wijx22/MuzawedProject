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
    path("branch-create/", views.branch_create, name="branch_create"),
    path("branch-delete/", views.branch_delete, name="branch_delete"),
    path("crete/request/", views.crete_request_view,  name='crete_request_view'),
    path('commercial-info/', views.add_commercial_info_view, name='commercial_info_form')
]
