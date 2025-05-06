from django.urls import path

from . import views

app_name = "supplier"

urlpatterns = [
    path("supplier-details/", views.supplier_details, name="supplier_details"),
    path("add_city/", views.add_city_view, name="add_city_view"),
    path('delete_city/<int:city_id>/', views.delete_city_view, name='delete_city_view'),
    path('cities/', views.cities_view, name='cities_view'),
    path("create/request/", views.supply_request_view,  name='supply_request_view'),
    path('update/supply_details/', views.update_supply_details_view, name='update_supply_details_view'),
    path('update/commercial_data/', views.update_commercial_data_view, name='update_commercial_data_view'),
    path('store_info/', views.store_info_view, name='store_info_view'),
    path('store/', views.store_view, name='store_view'),
    
    path("dashboard/reports/", views.supplier_reports_dashboard, name="reports_dashboard"),
    path("dashboard/reports/revenue/", views.report_revenue_by_product, name="report_revenue"),
    path("dashboard/reports/user-behavior/", views.report_user_behavior, name="report_user_behavior"),
    path("dashboard/reports/product-performance/", views.report_product_performance, name="report_product_performance"),
    
]
