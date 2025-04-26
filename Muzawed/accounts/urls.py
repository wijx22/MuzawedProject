from django.urls import path
from . import views


app_name = 'accounts' 

urlpatterns = [
  path('signup/', views.sign_up_beneficiary, name='sign_up_beneficiary'),
  path('signup/supplier/', views.sign_up_supplier, name='sign_up_supplier'),
  path('signin/', views.sign_in, name="sign_in"),
  path('logout/', views.log_out, name="log_out"),

  path('profile/<user_name>/', views.beneficiary_profile_view, name="beneficiary_profile_view"),
  path('update/profile', views.update_beneficiary_profile, name='update_beneficiary_profile'),
  
  path('profile/supplier/<user_name>/', views.supplier_profile_view, name='supplier_profile_view'),
  path('update/profile/supplier', views.update_supplier_profile, name='update_supplier_profile'),



]
