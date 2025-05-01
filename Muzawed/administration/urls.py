from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
  path('supplier/requests/', views.supplier_requests_list, name='supplier_requests_list'),


  path('admin/', views.dashboard, name='dashboard'),
  path('suppliers/', views.suppliers_list_view, name='suppliers_list_view'),
  path('beneficiary/', views.beneficiary_list_view, name='beneficiary_list_view'),
  path('contact-messages/', views.contact_messages_list_view, name='contact_messages_list'),
  path('reports/', views.report_list_view, name='report_list'),
  path('reply/<int:report_id>/', views.reply_to_report_view, name='reply_to_report_view'),
  path('reports/<int:report_id>/replies/', views.view_report_replies, name='view_report_replies'),
  path('supplier_requests_view/', views.supplier_requests_list, name='supplier_requests_view'),
  path('supplier/detail/<int:supplier_id>', views.supplier_request_detail, name='supplier_request_detail'),
  path('suppliers/<int:supplier_id>/approve/', views.approve_supplier_view, name='approve_supplier'),
  path('supplier/reject/<int:supplier_id>/', views.reject_supplier_view, name='reject_supplier'),
  path('supplier/products/view/<int:supplier_id>/', views.supplier_products_view, name='supplier_products_view'),
  #path('order/list/', views.order_requests_list, name='order_requests_list')
  #path('supplier/<int:supplier_id>/update_status/', views.update_supplier_status, name='update_supplier_status'),






]
