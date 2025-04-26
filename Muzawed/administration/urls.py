from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
  path('admin/', views.dashboard, name='dashboard'),
  path('suppliers/', views.suppliers_list_view, name='suppliers_list_view'),
  path('beneficiary/', views.beneficiary_list_view, name='beneficiary_list_view'),
  path('contact-messages/', views.contact_messages_list_view, name='contact_messages_list'),


]
