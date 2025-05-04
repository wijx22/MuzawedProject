from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('contact/', views.contact_view, name='contact_view'),
    path('about/', views.about_view, name='about_view'),
    path('supplier/', views.index_view, name='index_view'),
    path('store-status-handler/', views.store_status_handler, name='store_status_handler'),
    path('profile/<int:supplier_id>/', views.supplier_profile_view, name='supplier_profile_view'),
]
