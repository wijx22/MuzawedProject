from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('pay/', views.payment_page, name='payment_page'),
]
