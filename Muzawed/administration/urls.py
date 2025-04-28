from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
  path('admin/', views.dashboard, name='dashboard'),
  path('suppliers/', views.suppliers_list_view, name='suppliers_list_view'),
  path('beneficiary/', views.beneficiary_list_view, name='beneficiary_list_view'),
  path('contact-messages/', views.contact_messages_list_view, name='contact_messages_list'),
  path('reports/', views.report_list_view, name='report_list'),
  path('reply/<int:report_id>/', views.reply_to_report_view, name='reply_to_report_view'),
  path('reports/<int:report_id>/replies/', views.view_report_replies, name='view_report_replies'),




]
