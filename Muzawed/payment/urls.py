from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment_gateway/<int:payment_id>/', views.payment_gateway, name='payment_gateway'),
    path('save-payment/', views.save_payment, name='save_payment'),
]