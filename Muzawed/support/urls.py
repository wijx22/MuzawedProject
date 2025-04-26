from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('reports/create/', views.create_report_view, name='create_report_view'),

]
