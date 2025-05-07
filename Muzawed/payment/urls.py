from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
   path('pay/', views.payment_page, name='payment_page'),
    path('save-payment/', views.save_payment, name='save_payment'),
]
