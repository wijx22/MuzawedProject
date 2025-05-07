from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
  

  path('admin/', views.dashboard, name='dashboard'),
  path('suppliers/', views.suppliers_list_view, name='suppliers_list_view'),
  path('beneficiary/', views.beneficiary_list_view, name='beneficiary_list_view'),
  path('beneficiaries/<int:beneficiary_id>/', views.beneficiary_detail_view, name='beneficiary_detail'),

  path('contact-messages/', views.contact_messages_list_view, name='contact_messages_list'),
  path('reports/', views.report_list_view, name='report_list'),
  path('reply/<int:report_id>/', views.reply_to_report_view, name='reply_to_report_view'),
  path('supplier_requests_view/', views.supplier_requests_list, name='supplier_requests_view'),
  path('supplier/detail/<int:supplier_id>', views.supplier_request_detail, name='supplier_request_detail'),
  path('suppliers/<int:supplier_id>/approve/', views.approve_supplier_view, name='approve_supplier'),
  path('supplier/reject/<int:supplier_id>/', views.reject_supplier_view, name='reject_supplier'),
  path('supplier/<int:supplier_id>/', views.supplier_detail_view, name='supplier_detail'),
  path('orders/', views.order_list_view, name='order_list'),
  path('orders/detail/<int:order_id>/', views.order_detail_view, name='order_detail_view')







]
