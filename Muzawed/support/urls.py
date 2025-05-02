from django.urls import path

from . import views

app_name = "support"

urlpatterns = [
    path("reports/create/", views.create_report, name="create_report"),


    path(
        "reports/<int:report_id>/replies/",
        views.view_report_replies,
        name="view_report_replies",
    )
]
