from django.urls import path

from . import views

app_name = "supplier"

urlpatterns = [
    path("supplier-details/", views.supplier_details, name="supplier_details"),
    path("branch-create/", views.branch_create, name="branch_create"),
    path("branch-delete/", views.branch_delete, name="branch_delete"),
    path("create/request/", views.create_supply_request,  name='create_supply_request'),
    path('supply_details/', views.supply_details_view, name='supply_details_view'),
    path('commercial_data/', views.commercial_data_view, name='commercial_data_view')
]
