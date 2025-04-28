from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('reports/create/', views.create_report_view, name='create_report_view'),

    #path('reports/', views.report_list_view, name='report_list'),
    #path('reply/<int:report_id>/', views.reply_to_report_view, name='reply_to_report_view'),


]
