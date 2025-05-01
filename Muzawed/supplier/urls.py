from django.urls import path

from . import views

app_name = "supplier"

urlpatterns = [
    path("supplier-details/", views.supplier_details, name="supplier_details"),
    path("add_city/", views.add_city_view, name="add_city_view"),
    path('delete_city/<int:city_id>/', views.delete_city_view, name='delete_city_view'),
    path("create/request/", views.create_supply_request,  name='create_supply_request'),
    path('supply_details/', views.supply_details_view, name='supply_details_view'),
    path('commercial_data/', views.commercial_data_view, name='commercial_data_view')
]
